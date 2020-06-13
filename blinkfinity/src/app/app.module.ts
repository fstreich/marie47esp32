import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ApiModule, Configuration, ConfigurationParameters} from './swagger/index';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ProgramComponent } from './program/program.component';
import { ThumbnailComponent } from './thumbnail/thumbnail.component';
import { BASE_PATH } from './swagger/variables';
import { EditProgramComponent } from './edit-program/edit-program.component';
import { HomeScreenComponent } from './home-screen/home-screen.component';

@NgModule({
  declarations: [
    AppComponent,
    ProgramComponent,
    ThumbnailComponent,
    EditProgramComponent,
    HomeScreenComponent
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
