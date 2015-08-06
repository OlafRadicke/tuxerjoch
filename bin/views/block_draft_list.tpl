% import datetime
        <div class="list-group">
        % for item in artikles["rows"]:
            <div class="list-group-item">
                <h4 class="list-group-item-heading"><a href="view_article/{{item["id"]}}">{{item["value"]["title"]}}</a></h4>

                <p class="text-right">

                    % if item["value"]["created"] == item["value"]["last_update"]:
                        % created_datetime = datetime.datetime.fromtimestamp( int(item["value"]["created"]) )
                        % str_created_datetime = created_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    <small>Erstellt: {{str_created_datetime}}</small><br>
                    %end

                    % if item["value"]["created"] != item["value"]["last_update"]:
                        % update_datetime = datetime.datetime.fromtimestamp( int(item["value"]["last_update"]) )
                        % str_update_datetime = update_datetime.strftime('%Y-%m-%d %H:%M:%S')
                    <small>Letzte Änderung: {{str_update_datetime}}</small>
                    % end
                </p>
                <p>{{!item["value"]["teaser"]}}
                    <br>
                    &#91;<a href="edit_article/{{item["id"]}}">bearbeiten</a>&#93;
                </p>
                <p>Kategorie:
                % for tag in item["value"]["tags"]:
                    <a href="tags/{{tag}}">{{tag}}</a>
                %end
                </p>
            </div>
        % end
        </div>
