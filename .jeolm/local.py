from jeolm.driver import ( DriverError,
    processing_target, )
from jeolm.driver.groups import GroupsDriver
from jeolm.driver.source_link import SourceLinkDriver

class Driver(GroupsDriver, SourceLinkDriver):

    @processing_target
    def _generate_body_special_chapter( self, target, record, special_item,
        *, preamble, header_info,
        _seen_targets,
    ):
        target_groups = target.flags.intersection(self.groups)
        if len(target_groups) > 1:
            raise DriverError
        if len(target_groups) == 0:
            if 'group' in special_item:
                group_flag = special_item['group']
            else:
                group_flag = target.path.name
            if group_flag not in self.groups:
                raise DriverError
            target = target.flags_union({group_flag})
        else:
            group_flag, = target_groups
        group = self.groups[group_flag]

        if 'root' in special_item:
            chapter_root = special_item['root']
        else:
            chapter_root = '/'
        target = target.path_derive(chapter_root)

        if 'no-chapter' not in target.flags:
            chapter = group['name']
            if 'code' in group:
                chapter += " (" + group['code'] + ")"
            yield self.VerbatimBodyItem(r"\chapter{" + chapter + "}")
        yield self.VerbatimBodyItem(
            r"\begin{jeolmlabelspace}{" + group_flag + r"}")
        yield from self._generate_body( target,
            preamble=preamble, header_info=header_info,
            _seen_targets=_seen_targets )
        yield self.VerbatimBodyItem(r"\end{jeolmlabelspace}")

