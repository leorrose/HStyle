import { Component, Input, OnInit } from '@angular/core';
import { TeamMember } from '../models/team-member';

@Component({
    selector: 'app-team-member-card',
    templateUrl: './team-member-card.component.html',
    styleUrls: ['./team-member-card.component.css']
})

export class TeamMemberCardComponent implements OnInit {
    @Input() teamMember: TeamMember;

    constructor() { }

    ngOnInit(): void {
    }

    /**
     * method to copy a value to clipboard
     * @param val the value to copy to clipboard
     */
    copyToClipBoard(val: string): void {
        // create invisible textarea element
        const selBox = document.createElement('textarea');
        selBox.style.position = 'fixed';
        selBox.style.left = '0';
        selBox.style.top = '0';
        selBox.style.opacity = '0';
        selBox.value = val;
        document.body.appendChild(selBox);

        // copy invisible textarea value to clipboard
        selBox.focus();
        selBox.select();
        document.execCommand('copy');

        // remove textarea element
        document.body.removeChild(selBox);
    }
}
