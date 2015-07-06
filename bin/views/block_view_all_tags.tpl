    <h3 class="text-center">Verwendete Schlagworte</h3>
    <p
        style="column-count: 3;
            -moz-column-count: 3;
            -webkit-column-count: 3">

        % for key in sorted( tag_statistics["statistics"].keys() ):
            <br><a href="../tags/{{key}}">{{key}}</a> ({{tag_statistics["statistics"][key]}}x)
        % end
    </p>
