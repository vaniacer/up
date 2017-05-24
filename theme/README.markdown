Directory Theme
===============

<img src="https://raw.githubusercontent.com/Barrowclift/Directory-Theme/master/screenshot.png">

Thanks to [jfrazelle](https://github.com/jfrazelle) for providing [the wonderful base theme](https://github.com/jfrazelle/directory-theme) which I used as my base.

The core reason for my fork and changes was to focus on NGINX and tweak a few visual aspects of the theme to better suit my own needs and play better with NGINX. The original theme, while great, only truly shined on Apache directory listing since NGINX currently doesn't support richer features such as MIME icons, search, etc. Because of this there was a lot of extra resources that would just be ignored on NGINX and resulted in a browsing experience that wasn't quite as visually nice as the equivalent running on Apache.

Dependencies
------------

To start, you're going to want to ensure that your NGINX installation was built including the [Fancy Index module](https://www.nginx.com/resources/wiki/modules/fancy_index/). In brief, this module provides some slight improvements over NGINX's vanilla `autoindex` and provides additional goodies like human-readable file sizes, date formatting, etc.

Install
-------

To install, clone or download this repository and put it at the root of your directory listing site in `/var/www/` or wherever you put the websites that you've added to NGINX. To hide the theme directory from your listing change the name to `.theme` as [jfrazelle](https://github.com/jfrazelle) did. At this time feel free to take a peek into footer.html and change the footer links to be your own Twitter account, blog, whatever.

Now for the last step, in your `sites-enabled` directory in NGINX you're going to want to `vim` into your directory listing site and paste this as the last chunk in your `server` block:

	root /var/www/${YOUR_PATH_HERE};
	charset utf-8;

	error_page 404 /.theme/404.html;
	# let non-html ending links point to the html file
	try_files $uri.html $uri $uri/ =404;

	location / {
	    auth_basic            "Restricted Area";
	    auth_basic_user_file  /etc/nginx/conf.d/.htpasswd;
	    fancyindex on;
	    fancyindex_exact_size off;
	    fancyindex_footer /.theme/footer.html;
	    fancyindex_header /.theme/header.html;
	    fancyindex_css_href /.theme/style.css;
	    fancyindex_time_format "%B %e, %Y";
	}

I'm unsure if having the vanialla `autoindex` enabled above this will screw with things, so to be safe remove that line if it was present before. Reload your page and you should now be using a nicer theme that can easily be tweaked to your own liking.