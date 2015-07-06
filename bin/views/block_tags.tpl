% import datetime
    <h4>Artikel zu Schlagwort <i>{{tag_name}}</i></h4>
    <p>

        <div class="list-group">
        % for item in article_of_tag["rows"]:
            <a
                class="list-group-item"
                href="../view_article/{{item["id"]}}" >{{item["value"]}}</a>
        % end
        </div>

    </p>
