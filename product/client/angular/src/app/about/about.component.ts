import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AboutComponent implements OnInit {
  text = "Dr. Irina Rabaev main research interests include the areas of computer vision and image processing with a focus on historical documents analysis."
  head = "Irina Rabaev"
  constructor() { }

  ngOnInit(): void {


  }

}
