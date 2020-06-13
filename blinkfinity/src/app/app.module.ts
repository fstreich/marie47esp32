import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ApiModule, Configuration, ConfigurationParameters} from './swagger/index';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ProgramComponent } from './program/program.component';
import { ThumbnailComponent } from './thumbnail/thumbnail.component';
import { BASE_PATH } from './swagger/variables';

@NgModule({
  declarations: [
    AppComponent,
    ProgramComponent,
    ThumbnailComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [
    {  provide: BASE_PATH, 
      useValue: '/api' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
