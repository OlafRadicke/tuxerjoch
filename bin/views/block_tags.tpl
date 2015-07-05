% import datetime
    <h2>Artikel zu Schlagwort <i>{{tag_name}}</i></h2>
    <p>
        <ul>
        % for item in article_of_tag["rows"]:
            <li><a href="../view_article/{{item["id"]}}"><i>{{item["value"]}}</i></a></li>
        % end
        </ul>
    </p>
