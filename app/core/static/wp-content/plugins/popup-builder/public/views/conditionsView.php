<?php
use sgpb\AdminHelper;
$defaultData = ConfigDataHelper::defaultData();
$defaultConditions = $defaultData['freeConditions'];
?>

<div class="sgpb-wrapper sgpb-conditions-description-wrapper">
	<div class="row">
		<div class="col-md-3">
			<label><?php _e('Condition', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Page operator', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Select countries', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
	</div>
	<div class="row form-group">
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox($defaultConditions, 'countries', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox(array('is' => __('Is', SG_POPUP_TEXT_DOMAIN), 'is-not' => __('Is not', SG_POPUP_TEXT_DOMAIN)), 'is', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<input type="text" class="sgpb-full-width-events form-control" value="<?php _e('Select needed countries', SG_POPUP_TEXT_DOMAIN);?>">
		</div>
		<div class="col-md-3">
			<a href="<?php echo SG_POPUP_GEO_TARGETING_URL;?>" target="_blank" class="btn btn-warning btn-xs sgpb-advanced-targeting-pro-label">
				<?php _e('UNLOCK OPTION', SG_POPUP_TEXT_DOMAIN);?>
			</a>
		</div>
	</div>
	<div class="row">
		<div class="col-md-3">
			<label><?php _e('Condition', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Page operator', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Select user devices', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
	</div>
	<div class="row form-group">
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox($defaultConditions, 'devices', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox(array('is' => __('Is', SG_POPUP_TEXT_DOMAIN), 'is-not' => __('Is not', SG_POPUP_TEXT_DOMAIN)), 'is', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<input type="text" class="sgpb-full-width-events form-control" value="<?php _e('Select needed countries', SG_POPUP_TEXT_DOMAIN);?>">
		</div>
		<div class="col-md-3">
			<a href="<?php echo SG_POPUP_ADVANCED_TARGETING_URL;?>" target="_blank" class="btn btn-warning btn-xs sgpb-advanced-targeting-pro-label">
				<?php _e('UNLOCK OPTION', SG_POPUP_TEXT_DOMAIN);?>
			</a>
		</div>
	</div>
	<div class="row">
		<div class="col-md-3">
			<label><?php _e('Condition', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Page operator', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Select user status', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
	</div>
	<div class="row form-group">
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox($defaultConditions, 'user-status', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox(array('is' => __('Is', SG_POPUP_TEXT_DOMAIN), 'is-not' => __('Is not', SG_POPUP_TEXT_DOMAIN)), 'is', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox(array('logged-in' => __('logged In', SG_POPUP_TEXT_DOMAIN)), 'logged-in', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<a href="<?php echo SG_POPUP_ADVANCED_TARGETING_URL;?>" target="_blank" class="btn btn-warning btn-xs sgpb-advanced-targeting-pro-label">
				<?php _e('UNLOCK OPTION', SG_POPUP_TEXT_DOMAIN);?>
			</a>
		</div>
	</div>
	<div class="row">
		<div class="col-md-3">
			<label><?php _e('Condition', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Page operator', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('Select user role', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
	</div>
	<div class="row form-group">
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox($defaultConditions, 'user-role', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox(array('is' => __('Is', SG_POPUP_TEXT_DOMAIN), 'is-not' => __('Is not', SG_POPUP_TEXT_DOMAIN)), 'is', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<input type="text" class="sgpb-full-width-events form-control" value="<?php _e('Administrator, subscriber, editor...', SG_POPUP_TEXT_DOMAIN);?>">
		</div>
		<div class="col-md-3">
			<a href="<?php echo SG_POPUP_ADVANCED_TARGETING_URL;?>" target="_blank" class="btn btn-warning btn-xs sgpb-advanced-targeting-pro-label">
				<?php _e('UNLOCK OPTION', SG_POPUP_TEXT_DOMAIN);?>
			</a>
		</div>
	</div>
	<div class="row">
		<div class="col-md-3">
			<label><?php _e('Condition', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
		<div class="col-md-3">
			<label><?php _e('is at least', SG_POPUP_TEXT_DOMAIN);?></label>
		</div>
	</div>
	<div class="row form-group">
		<div class="col-md-3">
			<?php echo AdminHelper::createSelectBox($defaultConditions, 'after-x', array('class' => 'js-sg-select2')); ?>
		</div>
		<div class="col-md-3">
			<input type="text" class="sgpb-full-width-events form-control" value="<?php _e('number of pages', SG_POPUP_TEXT_DOMAIN);?>">
		</div>
		<div class="col-md-3">
			<a href="<?php echo SG_POPUP_ADVANCED_TARGETING_URL;?>" target="_blank" class="btn btn-warning btn-xs sgpb-advanced-targeting-pro-label">
				<?php _e('UNLOCK OPTION', SG_POPUP_TEXT_DOMAIN);?>
			</a>
		</div>
	</div>
</div>
<div class="sgpb-other-pro-options">
	<div class="row">
		<div class="col-md-12">
		</div>
	</div>
</div>
<style type="text/css">
	.sgpb-conditions-description-wrapper + .sgpb-other-pro-options {
		z-index: 9999;
	}

	.sgpb-advanced-targeting-pro-label,
	.sgpb-conditions-description-wrapper label {
		position: relative;
		z-index: 99990 !important;
	}
	.sgpb-advanced-targeting-pro-label {
		line-height: 21px;
	}
</style>

