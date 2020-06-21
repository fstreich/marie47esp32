import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { Pattern } from '../swagger/model/pattern';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';


@Component({
  selector: 'app-edit-pattern',
  templateUrl: './edit-pattern.component.html',
  styleUrls: ['./edit-pattern.component.css']
})

export class EditPatternComponent implements OnInit {

  @Output() dismiss = new EventEmitter <boolean>();
  @Input() pattern : Pattern ;
  @Input() number : number ;
  
  possibleClasses : string[] = [ 
  	'stripes', 'stars', 'random walk'
  ]

  possibleBlendModes : string[] = ['add', 'overlay'];

  constructor(  ) { }

  ngOnInit(): void {
  }

  close(): void{
  	this.dismiss.emit(true);
  }

}
