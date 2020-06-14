import { Component, OnInit, Input } from '@angular/core';
import { Pattern } from '../swagger/model/pattern';

@Component({
  selector: 'app-edit-pattern',
  templateUrl: './edit-pattern.component.html',
  styleUrls: ['./edit-pattern.component.css']
})
export class EditPatternComponent implements OnInit {

  @Input() pattern : any ;
  
  possibleClasses : string[] = [ 
  	'stripes', 'stars', 'random walk'
  ]

  constructor() { }

  ngOnInit(): void {
  }

}
