
% import datetime
<?xml version="1.0" encoding="utf-8"?>

<rss version="2.0">

    <channel>
        <title>{{hostname}}</title>
        <link>http://{{hostname}}</link>
        <description>Aktuelle Blog Posts</description>
        <language>de-de</language>
        <copyright>http://{{hostname}}</copyright>
        % current_time = datetime.datetime.now(datetime.timezone.utc)
        <pubDate>{{current_time.strftime('%a, %d %b %Y %H:%M:%S +0000')}}</pubDate>

        %for post in artikles:

        % last_update = datetime.datetime.fromtimestamp(int(post["value"]["last_update"]))
        % str_date = last_update.strftime('%Y-%m-%d %H:%M:%S')
        <item>
            <title><![CDATA[{{post["value"]["title"]}}]]></title>
            <description><![CDATA[{{post["value"]["teaser"]}}]]></description>
            <link>http://{{hostname}}/view_article/{{post["id"]}}</link>
            <author>http://{{hostname}}</author>
            <guid>http://{{hostname}}/view_article/{{post["id"]}}</guid>
            <pubDate>{{last_update.strftime('%a, %d %b %Y %H:%M:%S +0000')}}</pubDate>
        </item>
        %end

    </channel>

</rss>
