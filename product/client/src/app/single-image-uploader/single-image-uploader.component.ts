import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-single-image-uploader',
  templateUrl: './single-image-uploader.component.html',
  styleUrls: ['./single-image-uploader.component.css']
})
export class SingleImageUploaderComponent implements OnInit {
  @Output()
  imageContent: EventEmitter<File> = new EventEmitter<File>();
  @Input()
  dropZoneText:string;

  files: File[] = [];


  constructor() { }

  ngOnInit(): void {
  }

  onSelect(event): void{
    this.files = [];
    this.files.push(...event.addedFiles);
    this.imageContent.emit(this.files[0]);
  }

  onRemove(event): void{
    this.files.splice(this.files.indexOf(event), 1);
    this.imageContent.emit(null);
  }
}
