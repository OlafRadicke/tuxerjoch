<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
  <head>
    <title>{{title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>

    <div class="row">
        <!-- Tile header -->
<!--        <div class="col-md-12  col-lg-offset-1"
            style="background-image: url('/pics/alpen.jpg');
                    background-size: contain;
                    background-repeat: no-repeat;">
                <h1 class="col-md-12 .text-center"><a href="/">TUXERJOCH</a></h1>
        </div>-->
        <div class="col-md-12 ">
            <img class="img-responsive center-block" src="/pics/alpen.jpg" />
            <h1 class="col-md-12 .text-center"><a href="/">TUXERJOCH</a></h1>
        </div>


        <!-- Menu -->
        <div class="col-md-12">
            <ul  class="pager"> <!--class="nav nav-pills">-->
                % if authenticated == None:
                <li role="presentation"><a href="login">login</a></li>
                % end
                % if authenticated == "true":
                <li role="presentation"><a href="new_article">Neuer Artikel</a></li>
                <li role="presentation"><a href="logout">logout</a></li>
                % end
            </ul>

<!--            <ul class="nav nav-pills">
              <li role="presentation" class="active"><a href="#">Home</a></li>
              <li role="presentation"><a href="#">Profile</a></li>
              <li role="presentation"><a href="#">Messages</a></li>
            </ul>-->

        </div>
        <!-- tags -->
        <div class="col-md-4">tags...</div>
        <!-- main areal -->
        <div class="col-md-4">

            {{!main_area}}
        </div>
    </div>


  </body>
</html>
