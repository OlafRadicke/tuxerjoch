% setdefault('uri_prefix', '')
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="{{uri_prefix}}bootstrap/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
<!-- Page header -->
    <div class="row">
        <div class="col-md-12 text-center">
            <img class="img-responsive center-block" src="/pics/alpen_small.jpg" />
            <h1 class="col-md-12 .text-center"><a href="/">TUXERJOCH</a></h1>
        </div>
    </div>
<!-- Menu -->
    <div class="row">
        <div class="col-md-12">
            <ul  class="pager"> <!--class="nav nav-pills">-->
                % if authenticated == None:
                <li role="presentation"><a href="{{uri_prefix}}login">login</a></li>
                % end
                % if authenticated == "true":
                <li role="presentation"><a href="{{uri_prefix}}new_article">Neuer Artikel</a></li>
                <li role="presentation"><a href="{{uri_prefix}}logout">logout</a></li>
                % end
            </ul>
        </div>
    </div>
<!-- Middle area -->
    <div class="row">
<!-- main area -->
        <div class="col-md-4  col-md-offset-2">
            {{!main_area}}
        </div>
<!-- tags -->
        <div class="col-md-4">
            <h3>Tags</h3>
            <ul  class="list-unstyled">
                <li><a href="{{uri_prefix}}login">EINS</a></li>
                <li><a href="{{uri_prefix}}login">ZWEI</a></li>
                <li><a href="{{uri_prefix}}login">DREI</a></li>
                <li><a href="{{uri_prefix}}login">VIER</a></li>
            </ul>
        </div>
    </div>


  </body>
</html>
