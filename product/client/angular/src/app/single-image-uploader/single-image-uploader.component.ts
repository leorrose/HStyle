import { Component, EventEmitter, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-single-image-uploader',
  templateUrl: './single-image-uploader.component.html',
  styleUrls: ['./single-image-uploader.component.css']
})
export class SingleImageUploaderComponent implements OnInit {
  @Output() imageContent: EventEmitter<string | ArrayBuffer> = new EventEmitter<string | ArrayBuffer>();
  files: File[] = [];


  constructor() { }

  ngOnInit(): void {
  }

  onSelect(event): void{
    this.files = [];
    this.files.push(...event.addedFiles);

    this.readFile(this.files[0]).then(fileContents => {
      this.imageContent.emit(fileContents);
    });
  }

  onRemove(event): void{
    this.files.splice(this.files.indexOf(event), 1);
    this.imageContent.emit('');
  }

  private async readFile(file: File): Promise<string | ArrayBuffer> {
    return new Promise<string | ArrayBuffer>((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = e => {
        return resolve((e.target as FileReader).result);
      };

      reader.onerror = e => {
        console.error(`FileReader failed on file ${file.name}.`);
        return reject(null);
      };

      if (!file) {
        console.error('No file to read.');
        return reject(null);
      }

      reader.readAsDataURL(file);
    });
  }
}
