    <h1>Letzte Artikel</h1>
    <p>
        <ul>
        % for item in artikles["rows"]:
            <li><a href="view_article/{{item["id"]}}">{{item["id"]}}</a></li>
        % end
        </ul>
    </p>
