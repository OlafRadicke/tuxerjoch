% import datetime
        <div class="list-group">
        % for item in artikles["rows"]:



            <div class="list-group-item">
                <h4 class="list-group-item-heading"><a href="view_article/{{item["id"]}}">{{item["value"]["title"]}}</a></h4>
                % datetime_object = datetime.datetime.fromtimestamp(int(item["value"]["last_update"]))
                % str_date = datetime_object.strftime('%Y-%m-%d %H:%M:%S')
                <p class="text-right"><small>Letzte Änderung: {{str_date}}</small></p>
                <p>{{item["value"]["teaser"]}} &#91;<a href="view_article/{{item["id"]}}">Weiterlesen...</a>&#93;</p>
                <p>Kategorie:
                % for tag in item["value"]["tags"]:
                    <a href="tags/{{tag}}">{{tag}}</a>
                %end
                </p>
            </div>
        % end
        </div>
