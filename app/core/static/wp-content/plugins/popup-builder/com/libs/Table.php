<?php

namespace sgpbDataTable;

use sgpb\SubscriptionPopup;
require_once(dirname(__FILE__).'/ListTable.php');
file_exists(SG_POPUP_CLASSES_POPUPS_PATH.'SubscriptionPopup.php') && require_once(SG_POPUP_CLASSES_POPUPS_PATH.'SubscriptionPopup.php');

class SGPBTable extends SGPBListTable
{
	protected $id = '';
	protected $columns = array();
	protected $displayColumns = array();
	protected $sortableColumns = array();
	protected $tablename = '';
	protected $rowsPerPage = 10;
	protected $initialOrder = array();
	private $previewPopup = false;

	public function __construct($id, $popupPreviewId = false)
	{
		$this->id = $id;
		$this->previewPopup = $popupPreviewId;
		parent::__construct(array(
			'singular'=> 'wp_'.$id, //singular label
			'plural' => 'wp_'.$id.'s', //plural label
			'ajax' => false
		));
	}

	public function setId($id)
	{
		$this->id = $id;
	}

	public function setRowsPerPage($rowsPerPage)
	{
		$this->rowsPerPage = $rowsPerPage;
	}

	public function setColumns($columns)
	{
		$this->columns = $columns;
	}

	public function getColumns()
	{
		return $this->columns;
	}

	public function setDisplayColumns($displayColumns)
	{
		$this->displayColumns = $displayColumns;
	}

	public function setSortableColumns($sortableColumns)
	{
		$this->sortableColumns = $sortableColumns;
	}

	public function setTablename($tablename)
	{
		$this->tablename = $tablename;
	}

	public function setInitialSort($orderableColumns)
	{
		$this->initialOrder = $orderableColumns;
	}

	public function get_columns()
	{
		return $this->displayColumns;
	}

	public function prepare_items()
	{
		global $wpdb;
		$table = $this->tablename;

		$query = 'SELECT '.implode(', ', $this->columns).' FROM '.$table;
		$this->customizeQuery($query);

		$totalItems = count($wpdb->get_results($query)); //return the total number of affected rows

		if ($this->previewPopup) {
			$totalItems -= 1;
		}
		$perPage = $this->rowsPerPage;

		$totalPages = ceil($totalItems/$perPage);

		$orderby = isset($_GET['orderby']) ? sanitize_text_field($_GET['orderby']) : 'ASC';
		$order = isset($_GET['order']) ? sanitize_text_field($_GET['order']) : '';

		if (isset($this->initialOrder) && empty($order)) {
			foreach ($this->initialOrder as $key => $value) {
				$order = $value;
				$orderby = $key;
			}
		}

		if (!empty($orderby) && !empty($order)) {
			$query .= ' ORDER BY '.$orderby.' '.$order;
		}

		$paged = isset($_GET["paged"]) ? (int)$_GET["paged"] : '';

		if (empty($paged) || !is_numeric($paged) || $paged <= 0) {
			$paged = 1;
		}

		//adjust the query to take pagination into account
		if (!empty($paged) && !empty($perPage)) {
			$offset = ($paged - 1) * $perPage;
			$query .= ' LIMIT '.(int)$offset.','.(int)$perPage;
		}

		$this->set_pagination_args(array(
			"total_items" => $totalItems,
			"total_pages" => $totalPages,
			"per_page" => $perPage,
		));

		$columns = $this->get_columns();
		$hidden = array();
		$sortable = $this->get_sortable_columns();
		$this->_column_headers = array($columns, $hidden, $sortable);
		$items = $wpdb->get_results($query, ARRAY_N);
		/*Remove popup data when its class does not exist.*/
		$this->customizeRowsData($items);

		$this->items = $items;
	}

	public function customizeRowsData(&$items) {

	}

	public function get_sortable_columns() {
		return $this->sortableColumns;
	}

	public function display_rows()
	{
		//get the records registered in the prepare_items method
		$records = $this->items;

		//get the columns registered in the get_columns and get_sortable_columns methods
		list($columns, $hidden) = $this->get_column_info();

		if (!empty($records)) {
			foreach($records as $rec) {
				echo '<tr>';

				$this->customizeRow($rec);
				for ($i = 0; $i<count($rec); $i++) {
					echo '<td>'.stripslashes($rec[$i]).'</td>';
				}

				echo '</tr>';
			}
		}
	}

	public function customizeRow(&$row)
	{

	}

	public function customizeQuery(&$query)
	{

	}

	public function __toString()
	{
		$this->prepare_items(); ?>
		<form method="get" id="posts-filter">
		<p class="search-box">
			 <input type="hidden" name="post_type" value="popupbuilder" />
			 <input type="hidden" name="page" value="subscribers" />
			 <?php $this->search_box('search', 'search_id'); ?>
		</p>
		<?php $this->display();?>
		</form>
		<?php
		return '';
	}

	// parent class method overriding
	public function extra_tablenav($which)
	{
		$subscriptionPopups = SubscriptionPopup::getAllSubscriptionForms();
		$subscribersDates = SubscriptionPopup::getAllSubscribersDate();
		$uniqueDates = array();
		foreach ($subscribersDates as $arr) {
			$uniqueDates[] = $arr;
		}
		$uniqueDates = array_unique($uniqueDates, SORT_REGULAR);
		$selectedPopup = '';
		$selectedDate = '';
		$dateList = '';
		$list = '';
		$selected = '';
		if (isset($_GET['sgpb-subscription-popup-id'])) {
			$selectedPopup = (int)$_GET['sgpb-subscription-popup-id'];
		}
		if (isset($_GET['sgpb-subscribers-date'])) {
			$selectedDate = esc_sql($_GET['sgpb-subscribers-date']);
		}
		?>
		<div class="alignleft actions daterangeactions">
			<label class="screen-reader-text" for="sgpb-subscription-popup"><?php _e('Filter by popup', SG_POPUP_TEXT_DOMAIN)?></label>
			<input type="hidden" class="sgpb-subscription-popup-id" name="sgpb-subscription-popup-id" value="<?php echo $selectedPopup;?>">
			<select name="sgpb-subscription-popup" id="sgpb-subscription-popup">
				<?php
				$list .= '<option value="all">'.__('All', SG_POPUP_TEXT_DOMAIN).'</option>';
				foreach ($subscriptionPopups as $popupId => $popupTitle) {
					if ($selectedPopup == $popupId) {
						$selected = ' selected';
					}
					else {
						$selected = '';
					}
					$list .= '<option value="'.esc_attr($popupId).'"'.$selected.'>'.$popupTitle.'</option>';
				}
				echo $list;
				?>
			</select>
			<label class="screen-reader-text" for="sgpb-subscribers-dates"><?php _e('Filter by date', SG_POPUP_TEXT_DOMAIN)?></label>
			<input type="hidden" class="sgpb-subscribers-date" name="sgpb-subscribers-date" value="<?php echo $selectedDate;?>">
			<select name="sgpb-subscribers-dates" id="sgpb-subscribers-dates">
				<?php
				$gotDateList = '';
				foreach ($uniqueDates as $date) {
					if ($selectedDate == $date['date-value']) {
						$selected = ' selected';
					}
					else {
						$selected = '';
					}
					$gotDateList .= '<option value="'.$date['date-value'].'"'.$selected.'>'.date('d F Y', strtotime($date['date-title'])).'</option>';
				}
				if (empty($subscribersDates)) {
					$gotDateList = '<option value="'.$date['date-value'].'"'.$selected.'>'.__('Date', SG_POPUP_TEXT_DOMAIN).'</option>';
				}
				echo $dateList.$gotDateList;
				?>
			</select>
			<input name="filter_action" id="post-query-submit" class="button" value="<?php _e('Filter', SG_POPUP_TEXT_DOMAIN)?>" type="submit">
		</div>
		<?php
	}
}
