import { Component, OnInit } from '@angular/core';
import { ThumbnailComponent } from '../thumbnail/thumbnail.component';

@Component({
  selector: 'app-home-screen',
  templateUrl: './home-screen.component.html',
  styleUrls: ['./home-screen.component.css']
})
export class HomeScreenComponent implements OnInit {
	installation : string;

  constructor() { }

  ngOnInit(): void {
  	this.installation = 'Infinity Mirror'
  }

}
