<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>{{title}}</title>
  </head>
  <body>
    <h1><a href="/">TUXERJOCH</a></h1>
    <ul>
% if authenticated == None:
        <li><a href="login">login</a></li>
% end
% if authenticated == "true":
        <li><a href="logout">logout</a></li>
% end
        <li><a href="new_article">Neuer Artikel</a></li>
    </ul>

    {{!main_areal}}

  </body>
</html>
