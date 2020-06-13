import { Component, OnInit, ViewChild, Input, ElementRef, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-thumbnail',
  templateUrl: './thumbnail.component.html',
  styleUrls: ['./thumbnail.component.css']
})
export class ThumbnailComponent implements AfterViewInit {

  @ViewChild('myCanvas', {static: false}) myCanvas;
  @Input() number: number;


  public context : CanvasRenderingContext2D;

  constructor() { }

  ngAfterViewInit(): void {
  	// let canvas = this.myCanvas;
  	// console.log("canvas:",canvas);

  	console.log()

    let canvas = this.myCanvas.nativeElement;

    this.context = canvas.getContext('2d');
    this.context.font = "30px Arial";
	this.context.strokeText(""+this.number,30,60);
  }

}