import { Component, OnInit } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'blinkfinity';
  installation = 'Kaleidoscope'

  ngOnInit(): void {
  	this.installation = 'Infinity Mirror'
  }
}
