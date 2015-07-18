% setdefault('uri_prefix', '')
% setdefault('flashed_message', '')
% setdefault('flashed_level', 'info')
<!--
Supported Level:
    primary
    success
    info
    warning
    danger
-->

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="{{uri_prefix}}bootstrap/css/bootstrap.min.css" rel="stylesheet">

<!--     <link rel="alternate" type="application/rss+xml"  href="/rss.xml" title="Changed Pages"> -->
  </head>
  <body>
<!-- Page flashed message -->
% if flashed_message != '':
    <div class="row">
        <div class="col-md-12 text-center">
            <div class="bg-{{flashed_level}}">
                <h1>{{ flashed_message }}</h1>
            </div>
        </div>
    </div>
% end
<!-- Page header -->
    <div class="row">
        <div class="col-md-12 text-center">
            <img class="img-responsive center-block" src="/pics/alpen_small.jpg" />
            <h1 class="col-md-12 .text-center"><a href="/"><t>THE INDEPENDENT FRIEND</t></a></h1>
        </div>
    </div>
<!-- Menu -->
    <div class="row">
        <div class="col-md-12">
            <ul  class="pager"> <!--class="nav nav-pills">-->
                <li role="presentation"><a href="{{uri_prefix}}all_tags">Schlagworte</a></li>
                % if authenticated == None:
                <li role="presentation"><a href="{{uri_prefix}}login">login</a></li>
                % end
                % if authenticated == "true":
                <li role="presentation"><a href="{{uri_prefix}}new_article">Neuer Artikel</a></li>
                <li role="presentation"><a href="{{uri_prefix}}config">Einstellung</a></li>
                <li role="presentation"><a href="{{uri_prefix}}logout">logout</a></li>
                % end
            </ul>
        </div>
    </div>
    <hr
        style="width: 80%;
            height: 4px;
            margin-left: auto;
            margin-right: auto;
            background-color:#FF0066;
            color:#FF0066;
            border: 0 none;">

<!-- main area -->
    <div class="row">
        <div class="col-md-6 col-md-offset-3">
        <!--<div class="col-md-4  col-md-offset-2">-->
            {{!main_area}}
        </div>
    </div>
<!-- footer -->
    <hr style="width: 80%;height: 2px;margin-left: auto; margin-right: auto; background-color:#FF0066; color:#FF0066; border: 0 none;">
    <div class="row">
        <div class="col-md-12 text-center">
            <a href="https://github.com/OlafRadicke/tuxerjoch">TUXERJOCH</a>
        </div>
    </div>


  </body>
</html>
