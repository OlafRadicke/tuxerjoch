
    <h1>{{artikle["title"]}}</h1>

    <p>
        {{!artikle["article_text"]}}
    </p>
    <p>
        <b>Schlagworte:</b>
        % for item in artikle["tags"]:
            <a href="tags/{{item}}">{{item}}</a> 
        % end
        <br>
        % if authenticated == "true":
        <a href="../edit_article/{{artikle["uri_id"]}}">Artikel bearbeiten</a>
        %end
    </p>
