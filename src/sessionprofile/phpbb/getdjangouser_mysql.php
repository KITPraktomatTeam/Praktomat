<?php

function GetDBSession()
{
  $dbSession = mysql_connect("localhost", "DBUSERNAME", "DBPASSWORD");
  if (!$dbSession)
  {
    throw new Exception("cannot connect to DBMS: " . mysql_error());
  }

  $dbSelected = mysql_select_db("DATABASENAME", $dbSession);
  if (!$dbSelected)
  {
    throw new Exception("cannot select DB: " . mysql_error());
  }

  return $dbSession;
}


function GetDjangoUser()
{
    $djangoSessionID = $_COOKIE['sessionid'];

    $dbSession = GetDBSession();
    $query =
      "SELECT auth_user.username as username, auth_user.email as email ".
      "  FROM auth_user, sessionprofile_sessionprofile sp" .
      " WHERE sp.session_id = '" . mysql_real_escape_string($djangoSessionID) . "' " .
      "   AND auth_user.id = sp.user_id";
    $queryID = mysql_query($query, $dbSession);

    if (!$queryID)
    {
      throw new Exception("Could not check whether user was logged in: " , mysql_error());
    }

    $row = mysql_fetch_array($queryID);
    if ($row)
    {
      return $row;
    }

    return null;
}

?>
