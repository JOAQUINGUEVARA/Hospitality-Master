<?php
class SgpbPopupExtensionRegister
{
	public static function register($pluginName, $classPath, $className, $options = array())
	{
		$registeredData = array();
		$registeredPlugins = get_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS');

		if(!empty($registeredPlugins)) {
			$registeredData = get_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS');
		}

		if (!empty($registeredData)) {
			$registeredData = json_decode($registeredData, true);
		}

		if(empty($registeredData)) {
			$registeredData = array();
		}

		if(empty($classPath) || empty($className)) {
			if(!empty($registeredData[$pluginName])) {
				/*Delete the plugin from the registered plugins' list if the class name or the class path is empty.*/
				unset($registeredData[$pluginName]);
				update_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS', $registeredData);
			}

			return;
		}
		$pluginData['classPath'] = $classPath;
		$pluginData['className'] = $className;
		$pluginData['options'] = $options;

		$registeredData[$pluginName] = $pluginData;
		$registeredData = json_encode($registeredData);

		update_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS', $registeredData);
	}

	public static function remove($pluginName)
	{
		$registeredPlugins = get_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS');

		if (!$registeredPlugins) {
			return false;
		}

		$registeredData = json_decode($registeredPlugins, true);

		if(empty($registeredData)) {
			return false;
		}

		if (empty($registeredData[$pluginName])) {
			return false;
		}
		unset($registeredData[$pluginName]);
		$registeredData = json_encode($registeredData);

		update_option('SG_POPUP_BUILDER_REGISTERED_PLUGINS', $registeredData);

		return true;
	}
}
