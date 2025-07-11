<?php
namespace sgpb;

class ConvertToNewVersion
{
	private $id;
	private $content = '';
	private $type;
	private $title;
	private $options;
	private $customOptions = array();

	public function setContent($content)
	{
		$this->content = $content;
	}

	public function getContent()
	{
		return $this->content;
	}

	public function setType($type)
	{
		if ($type == 'shortcode') {
			$type = 'html';
		}
		$this->type = $type;
	}

	public function getType()
	{
		return $this->type;
	}

	public function setTitle($title)
	{
		$this->title = $title;
	}

	public function getTitle()
	{
		return $this->title;
	}

	public function setId($id)
	{
		$this->id = (int)$id;
	}

	public function getId()
	{
		return $this->id;
	}

	public function setOptions($options)
	{
		$this->options = $options;
	}

	public function getOptions()
	{
		return $this->options;
	}

	public function setCustomOptions($customOptions)
	{
		$this->customOptions = $customOptions;
	}

	public function getCustomOptions()
	{
		return $this->customOptions;
	}

	public static function convert()
	{
		$obj = new self();
		$obj->insertDataToNew();
	}

	public function insertDataToNew()
	{
		$idsMapping = array();
		Installer::install();
		Installer::registerPlugin();
		$popups = $this->getAllSavedPopups();
		$this->convertSettings();

		$arr = array();
		$popupPreviewId = get_option('popupPreviewId');
		foreach ($popups as $popup) {
			if (empty($popup)) {
				continue;
			}
			// we should not convert preview popup
			if ($popup['id'] == $popupPreviewId) {
				continue;
			}

			$popupObj = $this->popupObjectFromArray($popup);
			$arr[] = $popupObj;
			$args = array(
				'post_title' => $popupObj->getTitle(),
				'post_content' => $popupObj->getContent(),
				'post_status' => 'publish',
				'post_type' => SG_POPUP_POST_TYPE
			);
			$id = $popupObj->getId();
			$newOptions = $this->getNewOptionsFormSavedData($popupObj);

			$newPopupId = @wp_insert_post($args);
			$newOptions['sgpb-post-id'] = $newPopupId;
			$this->saveOtherOptions($newOptions);

			update_post_meta($newPopupId, 'sg_popup_options', $newOptions);
			$idsMapping[$id] = $newPopupId;
		}

		$this->convertCounter($idsMapping);

		update_option('sgpbConvertedIds', $idsMapping);

		return $arr;
	}

	/**
	 * Convert settings section saved options to new version
	 *
	 * @since 2.6.7.6
	 *
	 * @return bool
	 */
	private function convertSettings()
	{
		global $wpdb;
		$settings = $wpdb->get_row('SELECT options FROM '.$wpdb->prefix .'sg_popup_settings WHERE id = 1', ARRAY_A);

		if (empty($settings['options'])) {
			return false;
		}
		$settings = json_decode($settings['options'], true);
		
		$deleteData = 0;
		
		if (!empty($settings['tables-delete-status'])) {
			$deleteData = 1;
		}
		$userRoles = $settings['plugin_users_role'];

		if (empty($userRoles) || !is_array($userRoles)) {
			$userRoles = array();
		}
		
		$userRoles = array_map(function($role) {
			// it's remove sgpb_ keyword from selected values
			$role = substr($role, 5, strlen($role)-1);
			
			return $role;
		}, $userRoles);
		
		update_option('sgpb-user-roles', $userRoles);
		update_option('sgpb-dont-delete-data', $deleteData);

		return true;
	}

	private function convertCounter($idsMapping)
	{
		$oldCounter = get_option('SgpbCounter');

		if (!$oldCounter) {
			return false;
		}
		$newCounter = array();
		foreach ($oldCounter as $key => $value) {
			$newId = @$idsMapping[$key];
			$newCounter[$newId] = $value;
		}

		update_option('SgpbCounter', $newCounter);

		return true;
	}


	private function getAllSavedPopups()
	{
		global $wpdb;

		$query = 'SELECT `id`, `type`, `title`, `options` from '.$wpdb->prefix.'sg_popup ORDER BY id';
		$popups = $wpdb->get_results($query, ARRAY_A);

		return $popups;
	}

	public function getNewOptionsFormSavedData($popup)
	{
		$options = $popup->getOptions();
		$customOptions = $popup->getCustomOptions();
		$options = array_merge($options, $customOptions);
		// return addons event from add_connections data
		$addonsEvent = $this->getAddonsEventFromPopup($popup);
		if ($addonsEvent) {
			$options = array_merge($options, $addonsEvent);
		}
		$options = $this->filterOptions($options);

		$names = $this->getNamesMapping();
		$newData = array();
		$type = $popup->getType();

		if (empty($names)) {
			return $newData;
		}

		$newData['sgpb-type'] = $type;
		
		foreach ($names as $oldName => $newName) {
			if (isset($options[$oldName])) {
				$optionName = $this->changeOldValues($oldName, $options[$oldName]);
				$newData[$newName] = $optionName;
			}
		}
		$newData['sgpb-enable-popup-overlay'] = 'on';
		$newData['sgpb-show-background'] = 'on';

		return $newData;
	}

	private function saveOtherOptions($options)
	{
		$popupId = (int)$options['sgpb-post-id'];
		
		if (isset($options['sgpb-option-exit-intent-enable'])) {
			$eventsInitialData = array(
				array(
					array(
						'param' => 'exitIntent',
						'value' => @$options['sgpb-option-exit-intent-type'],
						'hiddenOption' => array(
							'sgpb-exit-intent-expire-time' => @$options['sgpb-exit-intent-expire-time'],
							'sgpb-exit-intent-cookie-level' => @$options['sgpb-exit-intent-cookie-level'],
							'sgpb-exit-intent-soft-from-top' => @$options['sgpb-exit-intent-soft-from-top']
						)
					)
				)
			);
			update_post_meta($popupId, 'sg_popup_events', $eventsInitialData);
		}
		else if(isset($options['sgpb-option-enable-ad-block'])) {
			$eventsInitialData = array(
				array(
					array(
						'param' => 'AdBlock',
						'value' => $options['sgpb-popup-delay'],
						'hiddenOption' => array()
					)
				)
			);
			update_post_meta($popupId, 'sg_popup_events', $eventsInitialData);
		}

		// MailChimp
		$mailchimpApiKey = get_option("SG_MAILCHIMP_API_KEY");

		if ($mailchimpApiKey) {
			update_option('SGPB_MAILCHIMP_API_KEY', $mailchimpApiKey);
		}

		// AWeber
		$aweberAccessToken = get_option('sgAccessToken');
		if ($aweberAccessToken) {
			$requestTokenSecret = get_option('requestTokenSecret');
			$accessTokenSecret = get_option('sgAccessTokenSecret');

			update_option('sgpbRequestTokenSecret', $requestTokenSecret);
			update_option('sgpbAccessTokenSecret', $accessTokenSecret);
			update_option('sgpbAccessToken', $aweberAccessToken);
		}

		return $options;
	}

	/**
	 * Get Addons options
	 *
	 * @param obj $popup
	 *
	 * @return bool|array
	 */
	private function getAddonsEventFromPopup($popup)
	{
		if (empty($popup)) {
			return false;
		}
		$popupId = $popup->getId();
		global $wpdb;

		$addonsOptionSqlString = 'SELECT options FROM '.$wpdb->prefix.'sg_popup_addons_connection WHERE popupId = %d and extensionType = "option"';
		$addonsSql = $wpdb->prepare($addonsOptionSqlString, $popupId);
		$results = $wpdb->get_results($addonsSql, ARRAY_A);

		if (empty($results)) {
			return false;
		}

		$options = array();

		// it's collect all events saved values ex Exit Intent and AdBlock
		foreach ($results as $result) {
			$currentOptions = json_decode($result['options'], true);

			if (empty($currentOptions)) {
				continue;
			}
			$options = array_merge($options, $currentOptions);
		}

		return $options;
	}

	/**
	 * Filter and change some related values for new version
	 *
	 * @param array $options
	 *
	 * @return array $options
	 */
	private function filterOptions($options)
	{
		if (@$options['effect'] != 'No effect') {
			$options['sgpb-open-animation'] = 'on';
		}

		if (isset($options['isActiveStatus']) && $options['isActiveStatus'] == 'off') {
			$options['isActiveStatus'] = '';
		}

		if (empty($options['sgTheme3BorderColor'])) {
			$options['sgTheme3BorderColor'] = '#000000';
		}
		
		if (@$options['popupContentBackgroundRepeat'] != 'no-repeat' && $options['popupContentBackgroundSize'] == 'auto') {
			$options['popupContentBackgroundSize'] = 'repeat';
		}
		$themeNumber = 1;

		if (isset($options['theme'])) {
			$themeNumber = preg_replace('/[^0-9]/', '', $options['theme']);
		}

		if (isset($options['aweber-success-behavior']) && $options['aweber-success-behavior'] == 'redirectToUrl') {
			$options['aweber-success-behavior'] = 'redirectToURL';
		}
		// if there is saved any extension option we do deactivate that popup
		if (isset($options['option-exit-intent-enable']) || isset($options['option-enable-ad-block'])) {
			$options['isActiveStatus'] = '';
		}
		
		if (isset($options['popup-content-padding'])) {
			// add theme default padding to content padding
			switch ($themeNumber) {
				case 1:
					$options['popup-content-padding'] += 7;
					break;
				case 4:
				case 6:
					$options['popup-content-padding'] += 12;
					break;
				case 2:
				case 3:
					$options['popup-content-padding'] += 0;
					break;
				case 5:
					$options['popup-content-padding'] += 5;
					break;
			}
		}

		switch ($themeNumber) {
			case 1:
				$buttonImageWidth = 21;
				$buttonImageHeight = 21;
				break;
			case 2:
				$buttonImageWidth = 20;
				$buttonImageHeight = 20;
				break;
			case 3:
				$buttonImageWidth = 38;
				$buttonImageHeight = 19;
				break;
			case 5:
				$buttonImageWidth = 17;
				$buttonImageHeight = 17;
				break;
			case 6:
				$buttonImageWidth = 30;
				$buttonImageHeight = 30;
				break;
			default:
				$buttonImageWidth = 0;
				$buttonImageHeight = 0;
		}

		$options['sgpb-button-image-width'] = $buttonImageWidth;
		$options['sgpb-button-image-height'] = $buttonImageHeight;

		return $options;
	}

	public function changeOldValues($optionName, $optionValue)
	{
		if ($optionName == 'theme') {
			$themeNumber = preg_replace('/[^0-9]/', '', $optionValue);
			$optionValue = 'sgpb-theme-'.$themeNumber;
		}

		return $optionValue;
	}

	private function popupObjectFromArray($arr)
	{
		global $wpdb;

		$options = json_decode($arr['options'], true);
		$type = $arr['type'];

		if (empty($type)) {
			return false;
		}

		$this->setId($arr['id']);
		$this->setType($type);
		$this->setTitle($arr['title']);
		$this->setContent('');
		
		switch ($type) {
			case 'image':
				$query = $wpdb->prepare('SELECT `url` FROM '.$wpdb->prefix.'sg_image_popup WHERE id = %d', $arr['id']);
				$result = $wpdb->get_row($query, ARRAY_A);

				if (!empty($result['url'])) {
					$options['image-url'] = $result['url'];
				}
				break;
			case 'html':
				$query = $wpdb->prepare('SELECT `content` FROM '.$wpdb->prefix.'sg_html_popup WHERE id = %d', $arr['id']);
				$result = $wpdb->get_row($query, ARRAY_A);

				if (!empty($result['content'])) {
					$this->setContent($result['content']);
				}
				break;
			case 'fblike':
				$query = $wpdb->prepare('SELECT `content`, `options` FROM '.$wpdb->prefix.'sg_fblike_popup WHERE id = %d', $arr['id']);
				$result = $wpdb->get_row($query, ARRAY_A);

				if (!empty($result['content'])) {
					$this->setContent($result['content']);
				}
				$customOptions = $result['options'];
				$customOptions = json_decode($customOptions, true);

				if (!empty($options)) {
					$this->setCustomOptions($customOptions);
				}
				break;
			case 'shortcode':
				$query = $wpdb->prepare('SELECT `url` FROM '.$wpdb->prefix.'sg_shortCode_popup WHERE id = %d', $arr['id']);
				$result = $wpdb->get_row($query, ARRAY_A);

				if (!empty($result['url'])) {
					$this->setContent($result['url']);
				}
				break;
			case 'mailchimp':
				$query = $wpdb->prepare('SELECT `content`, `options` FROM '.$wpdb->prefix.'sg_popup_mailchimp WHERE id = %d', $arr['id']);
				$result = $wpdb->get_row($query, ARRAY_A);

				if (!empty($result['content'])) {
					$this->setContent($result['content']);
				}

				$customOptions = $result['options'];
				$customOptions = json_decode($customOptions, true);

				if (!empty($options)) {
					$this->setCustomOptions($customOptions);
				}
				break;
			case 'aweber':
				$query = $wpdb->prepare('SELECT `content`, `options` FROM '.$wpdb->prefix.'sg_popup_aweber WHERE id = %d', $arr['id']);
				$result = $wpdb->get_row($query, ARRAY_A);

				if (!empty($result['content'])) {
					$this->setContent($result['content']);
				}

				$customOptions = $result['options'];
				$customOptions = json_decode($customOptions, true);

				if (!empty($options)) {
					$this->setCustomOptions($customOptions);
				}
				break;
		}

		$this->setOptions($options);

		return $this;
	}

	public function getNamesMapping()
	{
		 $names = array(
			 'type' => 'sgpb-type',
			 'delay' => 'sgpb-popup-delay',
			 'isActiveStatus' => 'sgpb-is-active',
			 'image-url' => 'sgpb-image-url',
			 'theme' => 'sgpb-popup-themes',
			 'effect' => 'sgpb-open-animation-effect',
			 'duration' => 'sgpb-open-animation-speed',
			 'popupOpenSound' => 'sgpb-open-sound',
			 'popupOpenSoundFile' => 'sgpb-sound-url',
			 'popup-dimension-mode' => 'sgpb-popup-dimension-mode',
			 'popup-responsive-dimension-measure' => 'sgpb-responsive-dimension-measure',
			 'width' => 'sgpb-width',
			 'height' => 'sgpb-height',
			 'maxWidth' => 'sgpb-max-width',
			 'maxHeight' => 'sgpb-max-height',
			 'escKey' => 'sgpb-esc-key',
			 'closeButton' => 'sgpb-enable-close-button',
			 'buttonDelayValue' => 'sgpb-close-button-delay',
			 'scrolling' => 'sgpb-enable-content-scrolling',
			 'disable-page-scrolling' => 'sgpb-disable-page-scrolling',
			 'overlayClose' => 'sgpb-overlay-click',
			 'contentClick' => 'sgpb-content-click',
			 'content-click-behavior' => 'sgpb-content-click-behavior',
			 'click-redirect-to-url' => 'sgpb-click-redirect-to-url',
			 'redirect-to-new-tab' => 'sgpb-redirect-to-new-tab',
			 'reopenAfterSubmission' => 'sgpb-reopen-after-form-submission',
			 'repeatPopup' => 'sgpb-show-popup-same-user',
			 'popup-appear-number-limit' => 'sgpb-show-popup-same-user-count',
			 'onceExpiresTime' => 'sgpb-show-popup-same-user-expiry',
			 'save-cookie-page-level' => 'sgpb-show-popup-same-user-page-level',
			 'popupContentBgImage' => 'sgpb-show-background',
			 'popupContentBackgroundSize' => 'sgpb-background-image-mode',
			 'popupContentBgImageUrl' => 'sgpb-background-image',
			 'sgOverlayColor' => 'sgpb-overlay-color',
			 'sg-content-background-color' => 'sgpb-background-color',
			 'popup-background-opacity' => 'sgpb-content-opacity',
			 'opacity' => 'sgpb-overlay-opacity',
			 'sgOverlayCustomClasss' => 'sgpb-overlay-custom-class',
			 'sgContentCustomClasss' => 'sgpb-content-custom-class',
			 'popup-z-index' => 'sgpb-popup-z-index',
			 'popup-content-padding' => 'sgpb-content-padding',
			 'popupFixed' => 'sgpb-popup-fixed',
			 'fixedPostion' => 'sgpb-popup-fixed-position',
			 'sgpb-open-animation' => 'sgpb-open-animation',
			 'theme-close-text' => 'sgpb-button-text',
			 'sgTheme3BorderRadius' => 'sgpb-border-radius',
			 'sgTheme3BorderColor' => 'sgpb-border-color',
			 'fblike-like-url' => 'sgpb-fblike-like-url',
			 'fblike-layout' => 'sgpb-fblike-layout',
			 'fblike-dont-show-share-button' => 'sgpb-fblike-dont-show-share-button',
			 'sgpb-button-image-width' => 'sgpb-button-image-width',
			 'sgpb-button-image-height' => 'sgpb-button-image-height'
		 );

		 // Exit Intent extension names
		$names['option-exit-intent-enable'] = 'sgpb-option-exit-intent-enable';
		$names['option-exit-intent-type'] = 'sgpb-option-exit-intent-type';
		$names['option-exit-intent-expire-time'] = 'sgpb-exit-intent-expire-time';
		$names['option-exit-intent-cookie-level'] = 'sgpb-exit-intent-cookie-level';
		$names['option-exit-intent-soft-from-top'] = 'sgpb-exit-intent-soft-from-top';
		
		// Adblock extension names
		$names['option-enable-ad-block'] = 'sgpb-option-enable-ad-block';

		// MailChimp extension names
		$names['mailchimp-list-id'] = 'sgpb-mailchimp-lists';
		$names['mailchimp-double-optin'] = 'sgpb-enable-double-optin';
		$names['mailchimp-only-required'] = 'sgpb-show-required-fields';
		$names['mailchimp-form-aligment'] = 'sgpb-mailchimp-form-align';
		$names['mailchimp-label-aligment'] = 'sgpb-mailchimp-label-alignment';
		$names['mailchimp-indicates-required-fields'] = 'sgpb-enable-asterisk-label';
		$names['mailchimp-asterisk-label'] = 'sgpb-mailchimp-asterisk-label';
		$names['mailchimp-required-error-message'] = 'sgpb-mailchimp-required-message';
		$names['mailchimp-email-validate-message'] = 'sgpb-mailchimp-email-message';
		$names['mailchimp-email-label'] = 'sgpb-mailchimp-email-label';
		$names['mailchimp-error-message'] = 'sgpb-mailchimp-error-message';
		$names['mailchimp-show-form-to-top'] = 'sgpb-mailchimp-show-form-to-top';
		$names['mailchimp-label-color'] = 'sgpb-mailchimp-label-color';
		$names['mailchimp-input-width'] = 'sgpb-mailchimp-input-width';
		$names['mailchimp-input-height'] = 'sgpb-mailchimp-input-height';
		$names['mailchimp-input-border-radius'] = 'sgpb-mailchimp-border-radius';
		$names['mailchimp-input-border-width'] = 'sgpb-mailchimp-border-width';
		$names['mailchimp-input-border-color'] = 'sgpb-mailchimp-border-color';
		$names['mailchimp-input-bg-color'] = 'sgpb-mailchimp-background-color';
		$names['sgpb-mailchimp-input-color'] = 'sgpb-mailchimp-input-color';
		$names['mailchimp-submit-title'] = 'sgpb-mailchimp-submit-title';
		$names['mailchimp-submit-width'] = 'sgpb-mailchimp-submit-width';
		$names['mailchimp-submit-height'] = 'sgpb-mailchimp-submit-height';
		$names['mailchimp-submit-border-width'] = 'sgpb-mailchimp-submit-border-width';
		$names['mailchimp-submit-border-radius'] = 'sgpb-mailchimp-submit-border-radius';
		$names['mailchimp-submit-border-color'] = 'sgpb-mailchimp-submit-border-color';
		$names['mailchimp-submit-button-bgcolor'] = 'sgpb-mailchimp-submit-background-color';
		$names['mailchimp-submit-color'] = 'sgpb-mailchimp-submit-color';
		$names['mailchimp-success-behavior'] = 'sgpb-mailchimp-success-behavior';
		$names['mailchimp-success-message'] = 'sgpb-mailchimp-success-message';
		$names['mailchimp-success-redirect-url'] = 'sgpb-mailchimp-success-redirect-URL';
		$names['mailchimp-success-redirect-new-tab'] = 'sgpb-mailchimp-success-redirect-new-tab';
		$names['mailchimp-success-popups-list'] = 'sgpb-mailchimp-success-popup';
		$names['mailchimp-close-popup-already-subscribed'] = 'sgpb-mailchimp-close-popup-already-subscribed';

		// AWeber extension
		$names['sg-aweber-list'] = 'sgpb-aweber-list';
		$names['sg-aweber-webform'] = 'sgpb-aweber-signup-form';
		$names['aweber-custom-invalid-email-message'] = 'sgpb-aweber-invalid-email';
		$names['aweber-invalid-email'] = 'sgpb-aweber-invalid-email-message';
		$names['aweber-already-subscribed-message'] = 'sgpb-aweber-custom-subscribed-message';
		$names['aweber-required-message'] = 'sgpb-aweber-required-message';
		$names['aweber-validate-email-message'] = 'sgpb-aweber-validate-email-message';
		$names['aweber-success-behavior'] = 'sgpb-aweber-success-behavior';
		$names['aweber-success-message'] = 'sgpb-aweber-success-message';
		$names['aweber-success-redirect-url'] = 'sgpb-aweber-success-redirect-URL';
		$names['aweber-success-redirect-new-tab'] = 'sgpb-aweber-success-redirect-new-tab';
		$names['aweber-success-popups-list'] = 'sgpb-aweber-success-popup';

		return $names;
	}

	public static function saveCustomInserted()
	{
		global $post;
		if (empty($post)) {
			return false;
		}

		$postId = $post->ID;
		if (get_option('sgpbSaveOldData'.$postId)) {
			return false;
		}

		update_option('sgpbSaveOldData'.$postId, 1);

		add_filter('sgpbConvertedPopupId', 'sgpb\sgpGetCorrectPopupId', 10, 1);
		self::saveMetaboxPopup($postId);
		$content = get_post_field('post_content', $postId);
		SGPopup::deletePostCustomInsertedData($postId);
		SGPopup::deletePostCustomInsertedEvents($postId);
		// We detect all the popups that were inserted as a custom ones, in the content.
		SGPopup::savePopupsFromContentClasses($content, $post);
	}

	public static function saveMetaboxPopup($postId)
	{
		$selectedPost = get_post_meta($postId, 'sg_promotional_popup', true);

		if (empty($selectedPost)) {
			return false;
		}
		global $SGPB_DATA_CONFIG_ARRAY;

		$postType = get_post_type($postId);
		$postTitle = get_the_title($postId);
		$popupId = sgpGetCorrectPopupId($selectedPost);
		$popupTargetParam = $postType.'_selected';

		if (!get_post_meta($popupId, 'sg_popup_events')) {
			update_post_meta($popupId, 'sg_popup_events', array($SGPB_DATA_CONFIG_ARRAY['events']['initialData']));
		}

		$savedTarget = get_post_meta($popupId, 'sg_popup_target');
		if (empty($savedTarget[0]['sgpb-target'][0])) {
			$savedTarget['sgpb-target'][] =  array(array('param' => $popupTargetParam, 'operator' => '==', 'value' => array($postId => $postTitle)));
			$savedTarget['sgpb-conditions'][] = $SGPB_DATA_CONFIG_ARRAY['conditions']['initialData'];

			update_post_meta($popupId, 'sg_popup_target', $savedTarget, true);
			return true;
		}
		$targets = $savedTarget[0]['sgpb-target'][0];
		$targetExists = false;

		foreach ($targets as $key => $target) {
			if ($key == 0 && $target['param'] == 'not_rule') {
				$target['param'] = $popupTargetParam;
				$savedTarget[0]['sgpb-target'][0][$key]['param'] = $popupTargetParam;
			}
			if ($target['param'] == $popupTargetParam) {
				$targetExists = true;
				$targetValue = array();
				if (!empty($target['value'])) {
					$targetValue = $target['value'];
				}

				$targetValue[$postId] = $postTitle;
				$savedTarget[0]['sgpb-target'][0][$key]['value'] = $targetValue;
				break;
			}
		}

		if (!$targetExists) {
			$savedTargetsLength = count($savedTarget[0]['sgpb-target'][0]);
			$savedTarget[0]['sgpb-target'][0][$savedTargetsLength] = array('param' => $popupTargetParam, 'operator' => '==', 'value' => array($postId => $postTitle));
		}

		delete_post_meta($postId, 'sg_promotional_popup');
		delete_post_meta($popupId, 'sg_popup_target');
		update_post_meta($popupId, 'sg_popup_target', $savedTarget[0], true);

		return true;
	}
}

function sgpGetCorrectPopupId($popupId)
{
	$convertedIds = get_option('sgpbConvertedIds');

	if (empty($convertedIds) || empty($convertedIds[$popupId])) {
		return $popupId;
	}

	return $convertedIds[$popupId];
}