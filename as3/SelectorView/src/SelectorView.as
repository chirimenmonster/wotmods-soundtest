package
{
	import net.wg.infrastructure.base.AbstractWindowView;
	import net.wg.infrastructure.events.LibraryLoaderEvent;

	import net.wg.gui.components.controls.ScrollBar;
	import net.wg.gui.components.controls.SoundButton;
	import net.wg.gui.components.controls.SoundListItemRenderer;
	
	import scaleform.clik.controls.Button;
	import scaleform.clik.controls.ListItemRenderer;
	import scaleform.clik.controls.ScrollingList;
	import scaleform.clik.controls.DropdownMenu;
	import scaleform.clik.data.ListData;
	import scaleform.clik.data.DataProvider;
	import scaleform.clik.events.ListEvent;

	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.text.TextField;
	import flash.text.TextFormat;
	import flash.text.TextFormatAlign;
	import flash.utils.getQualifiedClassName;
	
	/**
	 * ...
	 * @author Chirimen
	 */
	public class SelectorView extends AbstractWindowView
	{
		private var className:String = null;
		private var _isLibrariesLoaded:Boolean = false;
		private var _settings:Object = null;
		private var _soundModesMenu:DropdownMenu = null;
		private var _genderSwitchMenu:DropdownMenu = null;
		private var _nationsMenu:DropdownMenu = null;
		private var _soundEventsMenu:DropdownMenu = null;
		
		public var onButtonClickS:Function = null;
		public var playSoundEvent:Function = null;
        public var getDropdownMenuData:Function = null;

		public function SelectorView() : void
		{
			className = getQualifiedClassName(this);
			App.instance.loaderMgr.addEventListener(LibraryLoaderEvent.LOADED_COMPLETED, onLoadedCompleted);
			App.instance.loaderMgr.loadLibraries(Vector.<String>([
				"guiControlsLobby.swf", 
				"guiControlsLobbyBattle.swf", 
				"guiControlsLobbyBattleDynamic.swf", 
				"guiControlsLobbyDynamic.swf", 
				"guiControlsLogin.swf", 
				"guiControlsLoginBattle.swf", 
				"guiControlsLoginBattleDynamic.swf"
			]));
			super();
            width = 480;
            height = 200;
		}

		public function as_setConfig(menuData:Object) : void
		{
			_settings = menuData;
			initControls();
		}
		
		private function onLoadedCompleted(event:LibraryLoaderEvent) : void
		{
			App.instance.loaderMgr.removeEventListener(LibraryLoaderEvent.LOADED, onLoadedCompleted);
			_isLibrariesLoaded = true;
			//initControls();
		}

		private function onPlayButtonClick() : void
		{
			var currentSelected:Object = {
				soundMode: 		_soundModesMenu.dataProvider[_soundModesMenu.selectedIndex],
				genderSwitch:	_genderSwitchMenu.dataProvider[_genderSwitchMenu.selectedIndex],
				nation: 		_nationsMenu.dataProvider[_nationsMenu.selectedIndex],
				soundEvent:		_soundEventsMenu.dataProvider[_soundEventsMenu.selectedIndex]
			};
			//onButtonClickS(currentSelected);
            playSoundEvent(currentSelected);
		}

		private function onDropdownListIndexChange(event:Event) : void
		{
			var target:DropdownMenu = event.target as DropdownMenu;
			var selected:* = target.dataProvider[target.selectedIndex];
		}

		private function initControls() : void
		{
            createSoundModesMenu(_settings.soundModes);
            createGenderSwitchMenu(_settings.genderSwitch);
            createNationsMenu(_settings.nations);
            createSoundEventsMenu(_settings.events);
            createPlayButton();
            //createScrollingList(_settings.soundModes);
            window.title = "Sound Test";
		}

		private function createPlayButton() : void
		{
			var setting:Object = {
				label:      "Play",
				width:      80,
				height:     24,
				x:          0,
				y:          0
			}
			var button:SoundButton = App.utils.classFactory.getComponent("ButtonNormal", SoundButton, setting);
			if (button) {
				button.addEventListener(MouseEvent.CLICK, onPlayButtonClick);
				addChild(button);
			}
		}
		
		private function createSoundModesMenu(data:Array) : void
		{
			var dataProvider:DataProvider = new DataProvider(data);
			var setting:Object = {
				x:					0,
				y:					24,
				width:				120,
				itemRenderer:		"DropDownListItemRendererSound",
				dropdown:			"DropdownMenu_ScrollingList",
				dataProvider:		dataProvider,
				menuRowCount:		dataProvider.length,
				scrollBar:			"ScrollBar",
				thumbOffsetBottom:	0,
				thumbOffsetTop:		0
			};
			var dropdownMenu:DropdownMenu = App.utils.classFactory.getComponent("DropdownMenuUI", DropdownMenu, setting);
            if (dropdownMenu) {
                //dropdownMenu.addEventListener(ListEvent.INDEX_CHANGE, onDropdownListIndexChange);
                addChild(dropdownMenu);
                _soundModesMenu = dropdownMenu;
            }
		}

		private function createGenderSwitchMenu(data:Array) : void
		{
			var dataProvider:DataProvider = new DataProvider(data);
			var setting:Object = {
				x:					120,
				y:					24,
				width:				80,
				itemRenderer:		"DropDownListItemRendererSound",
				dropdown:			"DropdownMenu_ScrollingList",
				dataProvider:		dataProvider,
				menuRowCount:		dataProvider.length,
				scrollBar:			"ScrollBar",
				thumbOffsetBottom:	0,
				thumbOffsetTop:		0
			};
			var dropdownMenu:DropdownMenu = App.utils.classFactory.getComponent("DropdownMenuUI", DropdownMenu, setting);
            if (dropdownMenu) {
                //dropdownMenu.addEventListener(ListEvent.INDEX_CHANGE, onDropdownListIndexChange);
                addChild(dropdownMenu);
                _genderSwitchMenu = dropdownMenu;
            }
		}

		private function createNationsMenu(data:Array) : void
		{
			var dataProvider:DataProvider = new DataProvider(data);
			var setting:Object = {
				x:					200,
				y:					24,
				width:				80,
				itemRenderer:		"DropDownListItemRendererSound",
				dropdown:			"DropdownMenu_ScrollingList",
				dataProvider:		dataProvider,
				menuRowCount:		dataProvider.length,
				scrollBar:			"ScrollBar",
				thumbOffsetBottom:	0,
				thumbOffsetTop:		0
			};
			var dropdownMenu:DropdownMenu = App.utils.classFactory.getComponent("DropdownMenuUI", DropdownMenu, setting);
            if (dropdownMenu) {
                //dropdownMenu.addEventListener(ListEvent.INDEX_CHANGE, onDropdownListIndexChange);
                addChild(dropdownMenu);
                _nationsMenu = dropdownMenu;
            }
		}

		private function createSoundEventsMenu(data:Array) : void
		{
			var dataProvider:DataProvider = new DataProvider(data);
			var setting:Object = {
				x:					0,
				y:					48,
				width:				480,
				itemRenderer:		"DropDownListItemRendererSound",
				dropdown:			"DropdownMenu_ScrollingList",
				dataProvider:		dataProvider,
				menuRowCount:		dataProvider.length,
				scrollBar:			"ScrollBar",
				thumbOffsetBottom:	0,
				thumbOffsetTop:		0
			};
			var dropdownMenu:DropdownMenu = App.utils.classFactory.getComponent("DropdownMenuUI", DropdownMenu, setting);
            if (dropdownMenu) {
                //dropdownMenu.addEventListener(ListEvent.INDEX_CHANGE, onDropdownListIndexChange);
                addChild(dropdownMenu);
                _soundEventsMenu = dropdownMenu;
            }
		}

        private function createScrollingList(data:Array) : void
        {
            var dataProvider:DataProvider = new DataProvider(data);
            // DropdownList.dropdown に相当するプロパティが必要かどうかは不明
            var settings:Object = {
                x:                  0,
                y:                  72,
                width:              200,
                height:             300,
                itemRenderer:       "DropDownListItemRendererSound",
                dataProvider:       dataProvider,
                rowCount:           dataProvider.length,
                rowHeight:          25,
                scrollBar:          "ScrollBar",
                thumbOffsetBottom:  0,
                thumbOffsetTop:     0
            }
            // リンクするコンポート名が ScrollingList かどうかは不明
            var scrollingList:ScrollingList = App.utils.classFactory.getComponent("ScrollingList", ScrollingList, settings);
            if (scrollingList) {
                DebugUtils.LOG_DEBUG_FORMAT("%s: %s", className, "createed scrollingList");
                addChild(scrollingList);
            }
        }		
		
	}
	
}