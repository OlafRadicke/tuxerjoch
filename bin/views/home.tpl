<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>Startseite</title>
  </head>
  <body>
    <h1>Menü</h1>

    <ul>
        <li><a href="new_article">Neuer Artikel</a></li>
    </ul>

    <h1>Letzte Artikel</h1>

    <p>
        <ul>
        % for item in artikles["rows"]:
            <li><a href="view_article/{{item["id"]}}">{{item["id"]}}</a></li>
        % end
        </ul>
    </p>
  </body>
</html>
