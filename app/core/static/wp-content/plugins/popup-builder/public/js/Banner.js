function SGPBBanner() {

}

SGPBBanner.prototype.init = function() {
	this.close();
};

SGPBBanner.prototype.close = function() {
	if (!jQuery('.sgpb-banner-wrapper').length) {
		return;
	}

	jQuery('.sgpb-info-close').click(function() {
		jQuery('.sgpb-banner-wrapper').remove();
	});

	jQuery('.sgpb-dont-show-again').click(function() {
		var data = {
			action: 'sgpb_close_banner',
			nonce: SGPB_JS_PARAMS.nonce,
		};

		jQuery.post(ajaxurl, data, function(response) {
			jQuery('.sgpb-banner-wrapper').remove();
		});
	});
};

jQuery(document).ready(function() {
	var banner = new SGPBBanner();
	banner.init();
});
