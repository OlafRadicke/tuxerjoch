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
