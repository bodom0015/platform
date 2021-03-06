import {Injectable} from '@angular/core';
import {AuthHttp} from 'angular2-jwt';
import {Observable} from 'rxjs/Observable';
import {ComparisonNode} from '../../models/mmbdb/ComparisonNode';
import {EveUtilities} from '../common/EveUtilities';

/**
 * This class provides methods for working with the comparison_phylo_tree_nodes
 * endpoint.
 */
@Injectable()
export class ComparisonNodeService {

    private comparisonNodesUrl: string = "/api/v2/comparison_phylo_tree_nodes"

    constructor(private authHttp: AuthHttp) {
    }

    /**
     * Given a URL that returns multiple ComparisonNode items, streams all of
     * the returned items, even if paginated.
     *
     * Args:
     *     url (string): The query URL.
     *
     * Returns:
     *      Observable<ComparisonNode[]> that'll publish a single array
     *      containing all of the matching nodes.
     */
    getPagedItems(url: string): Observable<ComparisonNode[]> {
        return EveUtilities.getAllItems(url, this.authHttp).map((nodes: any[]) => {
            return nodes.map((node: any) => new ComparisonNode(
                node._id,
                node.node_name,
                node.node_level,
                node.comparison_id,
                node.node_idx,
                node.parent_node_idx,
                node.top_fst_otu_rankings_in_node
            ));
        });
    }

    /**
     * Returns the ComparisonNodes for a specified comparison and array of
     * taxonomy levels.
     *
     * Args:
     *     comparisonId (string): The comparison_id value to match.
     *     levels (string[]): An array of node_level values to match.
     *
     * Returns:
     *      Observable<ComparisonNode[]> that'll publish a single array
     *      containing all of the matching nodes.
     */
    getNodesForLevels(comparisonId: string, levels: string[]): Observable<ComparisonNode[]> {
        var url: string = this.comparisonNodesUrl + '?' +
                'comparison_id=' + comparisonId + '&' +
                levels.map((level) => 'node_level=' + level + '&').join();
		url = url.substring(0, url.length - 1)
        return this.getPagedItems(url);
    }

    /**
     * Given an array of ComparisonNodes, returns all of their children.
     *
     * Args:
     *     parents (ComparisonNode[]): The parent nodes.
     *
     * Returns:
     *      Observable<ComparisonNode[]> that'll publish a single array
     *      containing all of the child nodes.
     */
    getChildren(parents: ComparisonNode[]): Observable<ComparisonNode[]> {
        var orTerms: String[] = parents.map((parent) => '{"comparison_id" : "' + parent.comparisonId + '", "parent_node_idx": ' + parent.nodeIdx + '}');
        var url: string = this.comparisonNodesUrl + '?where={"$or": [' + orTerms.join() + ']}';
        return this.getPagedItems(url);
    }
}
