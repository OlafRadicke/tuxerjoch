% import datetime
    <p>
        % for item in artikles["rows"]:
            <h2><a href="view_article/{{item["id"]}}">{{item["value"]["title"]}}</a></h2>
            % datetime_object = datetime.datetime.fromtimestamp(int(item["value"]["last_update"]))
            % str_date = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
            <p class="text-right"><small>Letzte Änderung: {{str_date}}</small></p>
            <p>{{item["value"]["teaser"]}} &#91;<a href="view_article/{{item["id"]}}">Weiterlesen...</a>&#93;</p>
            <p>Kategorie:
            % for tag in item["value"]["tags"]:
<a href="tags/{{tag}}">{{tag}}</a>
            % end
    </p>
