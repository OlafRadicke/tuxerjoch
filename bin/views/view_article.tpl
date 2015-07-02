<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
% include('header.tpl', title='Artikel')
  <body>
% include( 'menu_bar.tpl', authenticated=authenticated )
    <h1>{{artikle["title"]}}</h1>

    <p>
{{artikle["article_text"]}}
    </p>

    <h2>Schlagworte</h2>

    <p>
        <ul>
        % for item in artikle["tags"]:
            <li><a href="tags/{{item}}">{{item}}</a></li>
        % end
        </ul>
    </p>
  </body>
</html>
