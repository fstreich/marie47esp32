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

  program : Program;
  id      : number; 

  constructor(private programService: ProgramService,
  		        private activatedRoute: ActivatedRoute,
              private router: Router ) {
  }

  ngOnInit(): void { 
  	this.id = this.activatedRoute.snapshot.params.id-1;
  	this.programService.programIdGet( this.id ).subscribe(
      (data) => { this.program = data }
    );
  }



  addPattern():void{
    this.program.patterns.push({ 
        pclass: "stars",
        name: "stars",
        speed: 5,
        hmirror: false,
        vmirror: false,
        rotate: 0,
        blender: 'add'
      } );
    this.programService.editPost( this.program ).subscribe(
      () => {}, // success: do nothing, 
      () => {}  // error: do nothing as well
    );
  }


  change(){
    this.programService.editPost( this.program ).subscribe(
      () => {},
      () => {}
    );
  }



  dismiss(index):void {
    this.program.patterns.splice(index,1);
  }



  cancel_edit() {
  	console.log("cancel edit button pressed...");
  	this.programService.endeditGet().subscribe();
  }



  saveProgram(){
    this.programService.programIdPost( this.program, this.id ).subscribe(
      () => { this.router.navigate(["home"]); },
      () => { this.router.navigate(["home"]); }
    );
  }
}
