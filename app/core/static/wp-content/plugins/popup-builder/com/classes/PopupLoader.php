<?php
namespace sgpb;
use \WP_Query;

class PopupLoader
{
	private static $instance;
	private $loadablePopups = array();
	private $loadablePopupsIds = array();

	private function __construct()
	{
		require_once(ABSPATH.'wp-admin/includes/plugin.php');
	}

	public static function instance() {

		if (!isset(self::$instance)) {
			self::$instance = new self;
		}

		return self::$instance;
	}

	public function setLoadablePopupsIds($loadablePopupsIds)
	{
		$this->loadablePopupsIds = $loadablePopupsIds;
	}

	public function getLoadablePopupsIds()
	{
		return $this->loadablePopupsIds;
	}

	public function addLoadablePopup($popupObj)
	{
		$this->loadablePopups[] = $popupObj;
	}

	public function setLoadablePopups($loadablePopups)
	{
		$this->loadablePopups = $loadablePopups;
	}

	public function getLoadablePopups()
	{
		return $this->loadablePopups;
	}

	public function addPopupFromUrl($popupsToLoad)
	{
		if (isset($_GET['sg_popup_id'])) {
			$getterId = (int)$_GET['sg_popup_id'];

			if (function_exists('sgpb\sgpGetCorrectPopupId')) {
				$getterId = sgpGetCorrectPopupId($getterId);
			}

			$popupFromUrl = SGPopup::find($getterId);
			if (!empty($popupFromUrl) && get_post_status($getterId) == 'publish') {
				global $SGPB_DATA_CONFIG_ARRAY;
				$defaultEvent = array();
				$customDelay = $popupFromUrl->getOptionValue('sgpb-popup-delay');
				$defaultEvent[] = $SGPB_DATA_CONFIG_ARRAY['events']['initialData'][0];
				$defaultEvent[0]['value'] = 0;
				if ($customDelay) {
					$defaultEvent[0]['value'] = $customDelay;
				}
				$popupFromUrl->setEvents($defaultEvent);
				$popupsToLoad[] = $popupFromUrl;
			}
		}

		return $popupsToLoad;
	}

	public function loadPopups()
	{
		$foundPopup = array();
		$popupPreviewArgs = array();
		if (is_preview()) {
			global $post;
			$foundPopup = $post;
		}
		// for the first time, when new wordpress with not changed theme
		if (isset($_GET['popup_preview_id'])) {
			$foundPopup = get_post($_GET['popup_preview_id']);
			$popupPreviewArgs = array('preview' => true);
		}
		if (!empty($foundPopup)) {
			global $SGPB_DATA_CONFIG_ARRAY;
			if (@$post->post_type == SG_POPUP_POST_TYPE) {
				$targets = array($SGPB_DATA_CONFIG_ARRAY['target']['initialData']);

				// for any targets preview popup should open
				if (!empty($targets[0][0])) {
					$targets[0][0]['param'] = 'post_all';
				}

				$popup = SGPopup::find($post);
				if (is_object($popup)) {
					$popup->setTarget($targets);
				}
			}
			if (@$foundPopup->post_type == SG_POPUP_POST_TYPE) {
				$popup = SGPopup::find($foundPopup, $popupPreviewArgs);

				$popup->setEvents($SGPB_DATA_CONFIG_ARRAY['events']['initialData'][0]);
				$this->addLoadablePopup($popup);
				$this->doGroupFiltersPopups();
				$popups = $this->getLoadablePopups();

				$scriptsLoader = new ScriptsLoader();
				$scriptsLoader->setLoadablePopups($popups);
				$scriptsLoader->loadToFooter();
				return;
			}
		}

		$popupBuilderPosts = new WP_Query(
			array(
				'post_type'      => SG_POPUP_POST_TYPE,
				'posts_per_page' => - 1
			)
		);
		// We check all the popups one by one to realize whether they might be loaded or not.
		while ($popupBuilderPosts->have_posts()) {
			$popupBuilderPosts->next_post();
			$popupPost = $popupBuilderPosts->post;
			$popup = SGPopup::find($popupPost);
			if (empty($popup)) {
				continue;
			}
			if ($popup->allowToLoad() || (is_preview() && get_post_type() == SG_POPUP_POST_TYPE)) {
				$this->addLoadablePopup($popup);
			}
		}


		$this->doGroupFiltersPopups();
		$popups = $this->getLoadablePopups();

		$scriptsLoader = new ScriptsLoader();
		$scriptsLoader->setLoadablePopups($popups);
		$scriptsLoader->loadToFooter();
	}

	private function doGroupFiltersPopups()
	{
		$popups = $this->getLoadablePopups();
		$popups = $this->addPopupFromUrl($popups);
		$groupObj = new PopupGroupFilter();
		$groupObj->setPopups($popups);
		$popups = $groupObj->filter();
		$this->setLoadablePopups($popups);
	}
}
