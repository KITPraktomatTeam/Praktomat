class SafeUncompressor(object):
	"""Small proxy class that enables external file object
	support for uncompressed, bzip2 and gzip files. Works transparently, and
	supports a maximum size to avoid zipbombs.
	"""
	blocksize = 16 * 1024

	class FileTooLarge(Exception):
		pass

	def __init__(self, fileobj, maxsize=10*1024*1024):
		self.fileobj = fileobj
		self.name = getattr(self.fileobj, "name", None)
		self.maxsize = maxsize
		self.init()

	def init(self):
		import bz2
		import gzip
		self.pos = 0
		self.fileobj.seek(0)
		self.buf = ""
		self.format = "plain"

		magic = self.fileobj.read(2)
		if magic == '\037\213':
			self.format = "gzip"
			self.gzipobj = gzip.GzipFile(fileobj = self.fileobj, mode = 'r')
		elif magic == 'BZ':
			raise IOError, "bzip2 support in SafeUncompressor disabled, as self.bz2obj.decompress is not safe"
			self.format = "bz2"
			self.bz2obj = bz2.BZ2Decompressor()
		self.fileobj.seek(0)
			

	def read(self, size):
		b = [self.buf]
		x = len(self.buf)
		while x < size:
			if self.format == 'gzip':
				data = self.gzipobj.read(self.blocksize)
				if not data:
					break
			elif self.format == 'bz2':
				raw = self.fileobj.read(self.blocksize)
				if not raw:
					break
				# this can already bomb here, to some extend.
				# so disable bzip support until resolved.
				# Also monitor http://stackoverflow.com/questions/13622706/how-to-protect-myself-from-a-gzip-or-bzip2-bomb for ideas
				data = self.bz2obj.decompress(raw)
			else:
				data = self.fileobj.read(self.blocksize)
				if not data:
					break
			b.append(data)
			x += len(data)

			if self.pos + x > self.maxsize:
				self.buf = ""
				self.pos = 0
				raise SafeUncompressor.FileTooLarge, "Compressed file too large"
		self.buf = "".join(b)

		buf = self.buf[:size]
		self.buf = self.buf[size:]
		self.pos += len(buf)
		return buf

	def seek(self, pos, whence=0):
		if whence != 0:
			raise IOError, "SafeUncompressor only supports whence=0"
		if pos < self.pos:
			self.init()
		self.read(pos - self.pos)

	def tell(self):
		return self.pos

	def write(self, data):
		self.pos += len(data)
		raw = self.bz2obj.compress(data)
		self.fileobj.write(raw)
