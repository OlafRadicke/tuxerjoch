% import datetime
    <h1>{{artikle["title"]}}</h1>
    <p class="text-right">
        % created_datetime = datetime.datetime.fromtimestamp( int(artikle["created"]) )
        % str_created_datetime = created_datetime.strftime('%Y-%m-%d %H:%M:%S')
        <small>Erstellt: {{str_created_datetime}}</small><br>
        % if artikle["created"] != artikle["last_update"]:
            % update_datetime = datetime.datetime.fromtimestamp( int(artikle["last_update"]) )
            % str_update_datetime = update_datetime.strftime('%Y-%m-%d %H:%M:%S')
        <small>Letzte Änderung: {{str_update_datetime}}</small>
        % end
    </p>

    <p>
        {{!artikle["article_text"]}}
    </p>
    <p>
        <b>Schlagworte:</b>
        % for item in artikle["tags"]:
            <a href="../tags/{{item}}">{{item}}</a>
        % end
        <br>
        % if authenticated == "true":
        <a href="../edit_article/{{artikle["uri_id"]}}">Artikel bearbeiten</a>
        %end
    </p>
