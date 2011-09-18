<?php
/**
* Django auth plug-in for phpBB3
*
* @package login
* @copyright (c) 2007 Resolver Systems
* @license http://opensource.org/licenses/gpl-license.php GNU Public License
*
*/

/**
* @ignore
*/
if (!defined('IN_PHPBB'))
{
  exit;
}

require_once("getdjangouser.php");


/**
 * Sanity check - don't let someone set the auth mode to use Django unless
 * they themselves are already logged into Django as a real phpBB user.
 *
 * @return boolean|string false if the user is identified and else an error message
 */
function init_django()
{
  global $user;

  $djangoUser = GetDjangoUser();
  if (!isset($djangoUser) || strtolower($user->data['username']) !== strtolower($djangoUser['username']))
  {
    return "You cannot set up Django authentication unless you are logged into Django";
  }
  return false;
}

/**
* Login function
*/
function login_django(&$username, &$password)
{
  global $db;

  // do not allow empty password
  if (!$password)
  {
    return array(
      'status'  => LOGIN_BREAK,
      'error_msg' => 'NO_PASSWORD_SUPPLIED',
    );
  }

  $djangoUser = GetDjangoUser();
  if (!isset($djangoUser))
  {
    return array(
      'status'    => LOGIN_ERROR_EXTERNAL_AUTH,
      'error_msg'   => 'LOGIN_ERROR_EXTERNAL_AUTH',
      'user_row'    => array('user_id' => ANONYMOUS),
    );
  }

  $php_auth_user = strtolower($djangoUser['username']);
  $php_auth_pw = "pretend password";

  if (!empty($php_auth_user) && !empty($php_auth_pw))
  {
    if ($php_auth_user !== strtolower($username))
    {
      return array(
        'status'  => LOGIN_ERROR_USERNAME,
        'error_msg' => 'LOGIN_ERROR_USERNAME',
        'user_row'  => array('user_id' => ANONYMOUS),
      );
    }

    $sql = 'SELECT user_id, username, user_password, user_passchg, user_email, user_type
      FROM ' . USERS_TABLE . "
      WHERE username = '" . $db->sql_escape($php_auth_user) . "'";
    $result = $db->sql_query($sql);
    $row = $db->sql_fetchrow($result);
    $db->sql_freeresult($result);

    if ($row)
    {
      // User inactive...
      if ($row['user_type'] == USER_INACTIVE || $row['user_type'] == USER_IGNORE)
      {
        return array(
          'status'    => LOGIN_ERROR_ACTIVE,
          'error_msg'   => 'ACTIVE_ERROR',
          'user_row'    => $row,
        );
      }

      // Successful login...
      return array(
        'status'    => LOGIN_SUCCESS,
        'error_msg'   => false,
        'user_row'    => $row,
      );
    }

    // this is the user's first login so create an empty profile
    return array(
      'status'    => LOGIN_SUCCESS_CREATE_PROFILE,
      'error_msg'   => false,
      'user_row'    => user_row_django($php_auth_user, $php_auth_pw),
    );
  }

  // Not logged into our website
  return array(
    'status'    => LOGIN_ERROR_EXTERNAL_AUTH,
    'error_msg'   => 'LOGIN_ERROR_EXTERNAL_AUTH',
    'user_row'    => array('user_id' => ANONYMOUS),
  );
}

/**
* Autologin function
*
* @return array containing the user row or empty if no auto login should take place
*/
function autologin_django()
{
  global $db;

  $djangoUser = GetDjangoUser();
  if (!isset($djangoUser))
  {
    return array();
  }

  $php_auth_user = strtolower($djangoUser['username']);
  $php_auth_email = $djangoUser['email'];
  $php_auth_pw = "pretend password";

  if (!empty($php_auth_user) && !empty($php_auth_pw))
  {
    set_var($php_auth_user, $php_auth_user, 'string');
    set_var($php_auth_email, $php_auth_email, 'string');
    set_var($php_auth_pw, $php_auth_pw, 'string');

    $sql = 'SELECT *
      FROM ' . USERS_TABLE . "
      WHERE username = '" . $db->sql_escape($php_auth_user) . "'";
    $result = $db->sql_query($sql);
    $row = $db->sql_fetchrow($result);
    $db->sql_freeresult($result);

    if ($row)
    {
      return ($row['user_type'] == USER_INACTIVE || $row['user_type'] == USER_IGNORE) ? array() : $row;
    }

    if (!function_exists('user_add'))
    {
      global $phpbb_root_path, $phpEx;

      include($phpbb_root_path . 'includes/functions_user.' . $phpEx);
    }

    // create the user if he does not exist yet
    user_add(user_row_django($php_auth_user, $php_auth_pw, $php_auth_email));

    $sql = 'SELECT *
      FROM ' . USERS_TABLE . "
      WHERE username_clean = '" . $db->sql_escape(utf8_clean_string($php_auth_user)) . "'";
    $result = $db->sql_query($sql);
    $row = $db->sql_fetchrow($result);
    $db->sql_freeresult($result);

    if ($row)
    {
      return $row;
    }
  }

  return array();
}

/**
* This function generates an array which can be passed to the user_add function in order to create a user
*/
function user_row_django($username, $password, $email)
{
  global $db, $config, $user;
  // first retrieve default group id
  $sql = 'SELECT group_id
    FROM ' . GROUPS_TABLE . "
    WHERE group_name = '" . $db->sql_escape('REGISTERED') . "'
      AND group_type = " . GROUP_SPECIAL;
  $result = $db->sql_query($sql);
  $row = $db->sql_fetchrow($result);
  $db->sql_freeresult($result);

  if (!$row)
  {
    trigger_error('NO_GROUP');
  }

  // generate user account data
  return array(
    'username'    => $username,
    'user_password' => phpbb_hash($password),
    'user_email'  => $email,
    'group_id'    => (int) $row['group_id'],
    'user_type'   => USER_NORMAL,
    'user_ip'   => $user->ip,
  );
}

/**
* The session validation function checks whether the user is still logged in
*
* @return boolean true if the given user is authenticated or false if the session should be closed
*/
function validate_session_django(&$user)
{
  $djangoUser = GetDjangoUser();
  if (!isset($djangoUser))
  {
    return false;
  }

  $php_auth_user = '';
  set_var($php_auth_user, strtolower($djangoUser['username']), 'string');

  return ($php_auth_user === strtolower($user['username'])) ? true : false;
}

?>
