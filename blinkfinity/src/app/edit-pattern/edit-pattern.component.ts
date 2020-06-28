import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Pattern } from '../swagger/model/pattern';
import { ProgramService } from '../swagger/api/program.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@Component({
  selector: 'app-edit-pattern',
  templateUrl: './edit-pattern.component.html',
  styleUrls: ['./edit-pattern.component.css']
})

export class EditPatternComponent implements OnInit {

  @Output() dismiss = new EventEmitter <boolean>();
  @Output() changed = new EventEmitter <boolean>();
  @Input() pattern : Pattern ;
  @Input() number : number ;
  
  possibleClasses : string[] = [ 
  	'stripes', 'stars', 'random walk'
  ]

  possibleBlendModes : string[] = ['add', 'overlay'];

  constructor( private programService: ProgramService ) { }

  ngOnInit(): void {
  }

  close(): void{
  	this.dismiss.emit(true);
  }

  // onChange(): void{
  // 	this.programService.editPost( this.program ).subscribe(
  //     () => {}, // success: do nothing, 
  //     () => {}  // error: do nothing as well
  //   );
  // }

}
