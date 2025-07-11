<?php

require_once(SG_POPUP_CLASSES_PATH.'/Ajax.php');
require_once(SG_POPUP_HELPERS_PATH.'AdminHelper.php');

use sgpb\SGPopup;
use sgpb\AdminHelper;
use sgpbDataTable\SGPBTable;

class Subscribers extends SGPBTable
{
	public function __construct()
	{
		global $wpdb;
		parent::__construct('');

		$this->setRowsPerPage(SGPB_APP_POPUP_TABLE_LIMIT);
		$this->setTablename($wpdb->prefix.SGPB_SUBSCRIBERS_TABLE_NAME);
		$this->setColumns(array(
			$this->tablename.'.id',
			'firstName',
			'lastName',
			'email',
			'cDate',
			$wpdb->prefix.SGPB_POSTS_TABLE_NAME.'.post_title AS subscriptionType'
		));
		$this->setDisplayColumns(array(
			'bulk'=>'<input class="subs-bulk" type="checkbox" autocomplete="off">',
			'id' => 'ID',
			'firstName' => __('First name', SG_POPUP_TEXT_DOMAIN),
			'lastName' => __('Last name', SG_POPUP_TEXT_DOMAIN),
			'email' => __('Email', SG_POPUP_TEXT_DOMAIN),
			'cDate' => __('Date', SG_POPUP_TEXT_DOMAIN),
			'subscriptionType' => __('Popup', SG_POPUP_TEXT_DOMAIN)
		));
		$this->setSortableColumns(array(
			'id' => array('id', false),
			'firstName' => array('firstName', true),
			'lastName' => array('lastName', true),
			'email' => array('email', true),
			'cDate' => array('cDate', true),
			'subscriptionType' => array('subscriptionType', true),
			$this->setInitialSort(array(
				'id' => 'DESC'
			))
		));
	}

	public function customizeRow(&$row)
	{
		$row[6] = $row[5];
		$row[5] = $row[4];
		$row[4] = $row[3];
		$row[3] = $row[2];
		$row[2] = $row[1];
		$row[1] = $row[0];

		// show date more user friendly
		$row[5] = date('d F Y', strtotime($row[5]));

		$id = $row[0];
		$row[0] = '<input type="checkbox" class="subs-delete-checkbox" data-delete-id="'.esc_attr($id).'">';
	}

	public function customizeQuery(&$query)
	{
		$query = AdminHelper::subscribersRelatedQuery($query);
	}
}
