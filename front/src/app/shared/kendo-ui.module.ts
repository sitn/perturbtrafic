import { NgModule } from '@angular/core';
import { DateInputsModule } from '@progress/kendo-angular-dateinputs';
import { DialogsModule } from '@progress/kendo-angular-dialog';
import { DropDownsModule } from '@progress/kendo-angular-dropdowns';
import { EditorModule } from '@progress/kendo-angular-editor';
import { GridModule } from '@progress/kendo-angular-grid';
import { InputsModule } from '@progress/kendo-angular-inputs';
import { TabStripModule } from '@progress/kendo-angular-layout';
import { MenusModule } from '@progress/kendo-angular-menu';
import { PopupModule } from '@progress/kendo-angular-popup';
import { ToolBarModule } from '@progress/kendo-angular-toolbar';


const COMPONENTS = [
  DropDownsModule,
  DateInputsModule,
  DialogsModule,
  InputsModule,
  EditorModule,
  ToolBarModule,
  TabStripModule,
  MenusModule,
  PopupModule,
  GridModule
];

@NgModule({
  imports: COMPONENTS,
  exports: COMPONENTS
})
export class KendoUiModule { }
