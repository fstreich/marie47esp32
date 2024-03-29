import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ApiModule, Configuration, ConfigurationParameters} from './swagger/index';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ThumbnailComponent } from './thumbnail/thumbnail.component';
import { BASE_PATH } from './swagger/variables';
import { EditProgramComponent } from './edit-program/edit-program.component';
import { HomeScreenComponent } from './home-screen/home-screen.component';
import { EditPatternComponent } from './edit-pattern/edit-pattern.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';

@NgModule({
  declarations: [
    AppComponent,
    ThumbnailComponent,
    EditProgramComponent,
    HomeScreenComponent,
    EditPatternComponent
  ],
  imports: [
  	ApiModule,
  	HttpClientModule,
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    AppRoutingModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production })
  ],
  providers: [
    {  provide: BASE_PATH, 
      useValue: '/api' }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
