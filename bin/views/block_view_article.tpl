
    <h1>{{artikle["title"]}}</h1>

    <p>
{{!artikle["article_text"]}}
    </p>

    <h2>Schlagworte</h2>

    <p>
        <ul>
        % for item in artikle["tags"]:
            <li><a href="tags/{{item}}">{{item}}</a></li>
        % end
        </ul>
    </p>
