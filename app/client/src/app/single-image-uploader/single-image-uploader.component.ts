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
    dropZoneText: string;
    files: File[] = [];

    constructor() { }

    ngOnInit(): void {
    }

    /**
     * method for image selection event
     * @param event the selection event
     */
    onSelect(event): void {
        // clean old image
        this.files = [];
        // add image to list
        this.files.push(...event.addedFiles);
        // emit the image
        this.imageContent.emit(this.files[0]);
    }

    /**
     * method for image removal event
     * @param event the removal event
     */
    onRemove(event): void {
        // remove image from list
        this.files.splice(this.files.indexOf(event), 1);
        // emit no image
        this.imageContent.emit(null);
    }
}
