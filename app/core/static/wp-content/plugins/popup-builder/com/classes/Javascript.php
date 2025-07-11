<?php
namespace sgpb;

/**
 * Popup Builder Style
 *
 * @since 2.5.6
 *
 * detect and include popup styles to the admin pages
 *
 */
class Javascript
{
	public static function enqueueScripts($hook)
	{
		$pageName = $hook;
		$scripts = array();
		$popupType = AdminHelper::getCurrentPopupType();
		$currentPostType = AdminHelper::getCurrentPostType();

		if($hook == 'popupbuilder_page_popupbuilder') {
			$pageName = 'popupType';
		}
		else if(($hook == 'post-new.php' || $hook == 'post.php') && $currentPostType == SG_POPUP_POST_TYPE) {
			$pageName = 'editpage';
		}
		else if($hook == 'edit.php' && !empty($currentPostType) && $currentPostType == SG_POPUP_POST_TYPE) {
			$pageName = 'popupspage';
		}
		else if ($hook == 'popupbuilder_page_subscribers') {
			$pageName = 'subscribers';
		}

		$registeredPlugins = get_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS');

		if(!$registeredPlugins) {
			return;
		}
		$registeredPlugins = json_decode($registeredPlugins, true);

		if(empty($registeredPlugins)) {
			return;
		}

		wp_enqueue_media();

		foreach($registeredPlugins as $pluginName => $pluginData) {

			if (!is_plugin_active($pluginName)) {
				continue;
			}

			if (empty($pluginData['classPath']) || empty($pluginData['className'])) {
				continue;
			}

			if (!file_exists($pluginData['classPath']))  {
				continue;
			}

			require_once($pluginData['classPath']);

			if (!class_exists($pluginData['className'])) {
				continue;
			}

			$classObj = new $pluginData['className']();
			$extensionInterface = 'SgpbIPopupExtension';

			if(!$classObj instanceof $extensionInterface) {
				continue;
			}
			$args  = array(
				'popupType' => $popupType
			);
			$scriptData = $classObj->getScripts($pageName , $args);

			$scripts[] = $scriptData;
		}

		if(empty($scripts)) {
			return;
		}

		foreach($scripts as $script) {
			if(empty($script['jsFiles'])) {
				continue;
			}

			foreach($script['jsFiles'] as $jsFile) {

				if(empty($jsFile['folderUrl'])) {
					wp_enqueue_script($jsFile['filename']);
					continue;
				}

				$dirUrl = $jsFile['folderUrl'];
				$dep = (!empty($jsFile['dep'])) ? $jsFile['dep'] : '';
				$ver = (!empty($jsFile['ver'])) ? $jsFile['ver'] : '';
				$inFooter = (!empty($jsFile['inFooter'])) ? $jsFile['inFooter'] : '';

				ScriptsIncluder::registerScript($jsFile['filename'], array(
					'dirUrl'=> $dirUrl,
					'dep' => $dep,
					'ver' => $ver,
					'inFooter' => $inFooter
					)
				);
				ScriptsIncluder::enqueueScript($jsFile['filename']);
			}

			if(empty($script['localizeData'])) {
				continue;
			}

			$localizeDatas = $script['localizeData'];

			foreach($localizeDatas  as $localizeData) {
				ScriptsIncluder::localizeScript($localizeData['handle'], $localizeData['name'], $localizeData['data']);
			}
		}
	}
}
