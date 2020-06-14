import { Component, OnInit } from '@angular/core';
import { EditPatternComponent } from '../edit-pattern/edit-pattern.component';
import { Pattern } from '../swagger/model/pattern';

@Component({
  selector: 'app-edit-program',
  templateUrl: './edit-program.component.html',
  styleUrls: ['./edit-program.component.css']
})
export class EditProgramComponent implements OnInit {

  name : string = "unnamed program";

  patterns : Pattern[] = [
  	{ _class: "stars", speed: 8},
  	{ _class: "stripes", speed: 2},
  	{ _class: "random walk", speed: 2},
  ];

  constructor() { }

  ngOnInit(): void {
  }

}
