import { TeamMemberService } from '../services/team-member.service';
import { TeamMember } from './../models/team-member';
import { Component, OnInit } from '@angular/core';

@Component({
    selector: 'app-team-members',
    templateUrl: './team-members.component.html',
    styleUrls: ['./team-members.component.css']
})
export class TeamMembersComponent implements OnInit {
    teamMembers: Array<TeamMember[]>;

    constructor(private teamMemberService: TeamMemberService) { }

    ngOnInit(): void {
        // create chunks of team members - each chunk is a row in html
        this.teamMembers = this.chunkArray(this.teamMemberService.getTeamMembers(), 3);
    }


    /**
     * method split array into chunks
     * @param array array of team members
     * @param size number of element in each chunk
     * @returns array of chunks (arrays of team members)
     */
    chunkArray(array: TeamMember[], size: number): Array<TeamMember[]> {
        // test array isn't empty
        if (array && array.length > 0){
            const result = [];
            // create copy to not change original
            const arrayCopy = [...array];

            // split array into chunks of same size
            while (arrayCopy.length > 0) {
                result.push(arrayCopy.splice(0, size));
            }

            // if last chunk is not size we push empty objects
            if (result[result.length - 1].length !== size) {
                const toAdd = size - result[result.length - 1].length;
                for (let i = 0; i < toAdd; i++) {
                    result[result.length - 1].push({});
                }
            }
            return result;
        }
        return [];
    }
}
