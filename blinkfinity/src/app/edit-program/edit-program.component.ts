import { Component, OnInit } from '@angular/core';
import { EditPatternComponent } from '../edit-pattern/edit-pattern.component';
import { Pattern } from '../swagger/model/pattern';
import { Program } from '../swagger/model/program';
import { ProgramService } from '../swagger/api/program.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-edit-program',
  templateUrl: './edit-program.component.html',
  styleUrls: ['./edit-program.component.css']
})
export class EditProgramComponent implements OnInit {

  name : string = "unnamed program";

  program : Program

  patterns : Pattern[] = [
  	{ _class: "stars", speed: 8},
  	{ _class: "stripes", speed: 2},
  	{ _class: "random walk", speed: 2},
  ];

  constructor(private programService: ProgramService,
  		      private activatedRoute: ActivatedRoute) {
  }

  ngOnInit(): void { 
  	let id = this.activatedRoute.snapshot.params.id;
  	this.programService.programIdGet( id ).subscribe(
      this.patterns

    );
  }

  cancel_edit() {
  	console.log("cancel edit button pressed...");
  	this.programService.endeditGet().subscribe();
  }
}
