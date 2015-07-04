    <h2>Verwendete Schlagworte</h2>
    <p>
        <dl class="dl-horizontal">
        % for key in sorted( tag_statistics.keys() ):
            <dt>{{tag_statistics[key]}}</dt>
            <dd><a href="../tags/{{key}}">{{key}}</a></dd>
        % end
        </dl>
    </p>
