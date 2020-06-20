import { Component, OnInit } from '@angular/core';
import { EditPatternComponent } from '../edit-pattern/edit-pattern.component';
import { Pattern } from '../swagger/model/pattern';
import { ProgramService } from '../swagger/api/program.service';

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

  constructor(private programService: ProgramService) {
  }

  ngOnInit(): void { 
  	let dings = this.programService.programIdGet(1,1) // TODO 
  }

  cancel_edit() {
  	console.log("cancel edit button pressed...");
  	this.programService.endeditGet().subscribe();
  }
}
