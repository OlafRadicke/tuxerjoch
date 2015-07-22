% import datetime
<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>{{hostname}}</title>
        <description>The latest Blog Posts</description>
        <link>http://{{hostname}}</link>
        <atom:link href="http://{{hostname}}/atom.xml" rel="self" type="application/atom+xml" />
        %for post in artikles:

        % last_update = datetime.datetime.fromtimestamp(int(post["value"]["last_update"]))
        % str_date = last_update.strftime('%Y-%m-%d %H:%M:%S')
        <item>
            <title>{{post["value"]["title"]}}</title>
            <link>http://{{hostname}}/view_article/{{post["id"]}}</link>
            <guid isPermaLink="true">http://{{hostname}}/view_article/{{post["id"]}}</guid>
            <pubDate>{{last_update.strftime('%a, %d %b %Y %H:%M:%S +0000')}}</pubDate>
            <description>{{post["value"]["teaser"]}}</description>
        </item>
        %end
    </channel>
</rss>
