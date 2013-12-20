delete from auth_permission where codename like 'add_%' or codename like 'change_%' or codename like 'delete_%';


delete from space_solution;
insert  into space_solution(id,name,description,is_active,registered_at,modified_in) values 
(1,'Shomware Basic','Limitado para ventas',1,'2013-10-31 04:52:44','2013-11-13 05:03:19');
insert  into space_solution(id,name,description,is_active,registered_at,modified_in) values 
(2,'Shomware Ultimate','Backend + Ventas',1,'2013-10-31 04:53:33','2013-10-31 04:53:33');

delete from sad_module;
insert  into `sad_module`(`id`,`module`,`name`,`is_active`,`icon`,`description`,`registered_at`,`modified_in`) values
(1,'DBM','Backend',1,NULL,'','2013-10-31 04:51:34','2013-11-10 16:57:52');
insert  into `sad_module`(`id`,`module`,`name`,`is_active`,`icon`,`description`,`registered_at`,`modified_in`) values
(2,'VENTAS','Ventas',1,NULL,'','2013-10-31 04:52:14','2013-11-13 05:03:15');
insert  into `sad_module`(`id`,`module`,`name`,`is_active`,`icon`,`description`,`registered_at`,`modified_in`) values
(3,'PRO','Profesional',1,NULL,'','2013-11-20 22:06:44','2013-11-20 22:06:44');

delete from sad_module_solutions;
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values 
(1,1,2);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(2,3,2);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(3,3,1);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(4,2,2);
insert  into `sad_module_solutions`(`id`,`module_id`,`solution_id`) values
(5,2,1);


delete from auth_group;
insert  into `auth_group`(`id`,`name`) values 
(1,'MASTER');
insert  into `auth_group`(`id`,`name`) values 
(2,'CATASTRO');
insert  into `auth_group`(`id`,`name`) values 
(3,'GERENTE VENTAS');
insert  into `auth_group`(`id`,`name`) values 
(4,'VENDEDOR');
insert  into `auth_group`(`id`,`name`) values 
(5,'RRHH');


delete from sad_module_groups;
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(1,1,1);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(2,1,2);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(3,3,5);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(4,2,4);
insert  into `sad_module_groups`(`id`,`module_id`,`group_id`) values 
(5,2,3);


delete from sad_module_initial_groups;
insert  into `sad_module_initial_groups`(`id`,`module_id`,`group_id`) values 
(1,1,1);
insert  into `sad_module_initial_groups`(`id`,`module_id`,`group_id`) values 
(2,3,5);
insert  into `sad_module_initial_groups`(`id`,`module_id`,`group_id`) values 
(3,2,3);


delete from django_content_type;
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values 
(1,'permission','auth','permission');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(2,'group','auth','group');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(3,'user','auth','user');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(4,'content type','contenttypes','contenttype');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(5,'session','sessions','session');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(6,'site','sites','site');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(7,'log entry','admin','logentry');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(8,'locality type','params','localitytype');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(9,'locality','params','locality');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(10,'person','params','person');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(11,'solution','space','solution');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(12,'association','space','association');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(13,'enterprise','space','enterprise');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(14,'headquart','space','headquart');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(15,'module','sad','module');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(16,'menu','sad','menu');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(17,'user profile enterprise','sad','userprofileenterprise');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(18,'user profile headquart','sad','userprofileheadquart');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(19,'user profile association','sad','userprofileassociation');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(20,'resource','sad','resource');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(21,'group','sad','group');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(22,'user','sad','user');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(23,'dashboard','mod_backend','dashboard');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(24,'dashboard','mod_ventas','dashboard');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(25,'categoria','params','categoria');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(26,'producto','maestros','producto');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(27,'','home','');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(28,'dashboard','mod_pro','dashboard');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(29,'employee','rrhh','employee');
insert  into `django_content_type`(`id`,`name`,`app_label`,`model`) values
(30,'profile','sad','profile');



delete from auth_permission;
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Puede hacer TODAS las oper. de tipos d localidades',8,'localitytype');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(2,'Puede hacer TODAS las operaciones de localidades',9,'locality');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(3,'Puede ver el index de localidades',9,'locality_index');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(4,'Puede agregar localidad',9,'locality_add');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(5,'Puede actualizar localidades',9,'locality_edit');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(6,'Puede eliminar localidades',9,'locality_delete');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(7,'Puede reportar localidades',9,'locality_report');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(8,'Puede inactivar y reactivar localidades',9,'locality_state');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(9,'Puede hacer TODAS las operaciones de personas',10,'person');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(10,'Puede hacer TODAS las operaciones de soluciones',11,'solution');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(11,'Puede hacer TODAS las operaciones de asociaciones',12,'association');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(12,'Puede hacer TODAS las operaciones de empresas',13,'enterprise');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(13,'Puede hacer TODAS las operaciones de sedes',14,'headquart');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(14,'Puede hacer TODAS las operaciones de modulos',15,'module');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(15,'Puede hacer TODAS las operaciones de menus',16,'menu');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(16,'Submodulo del sistema para la gestion de los recur',20,'resource');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(17,'Submodulo del sistema para los perfiles de usuario',21,'group');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(18,'Submodulo para la administracion de los usuarios d',22,'user');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(19,'Dashboard del mod_backend',23,'dashboard');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(20,'Dashboard del mod_ventas',24,'dashboard');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(54,'Puede hacer TODAS las operaciones de categorias',25,'categoria');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(85,'Puede hacer TODAS las operaciones de productos',26,'producto');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(86,'Puede ver el index de productos',26,'producto_index');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(87,'Puede agregar producto',26,'producto_add');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(88,'Puede actualizar productos',26,'producto_edit');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(89,'Puede eliminar productos',26,'producto_delete');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(90,'Puede reportar productos',26,'producto_report');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(91,'Puede inactivar y reactivar productos',26,'producto_state');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(92,'Puede actualizar precio venta de productos',26,'producto_edit_precio');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(93,'Todo',27,'');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(94,'mod_pro',28,'dashboard');
insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values
(161,'Puede hacer TODAS las operaciones de empleados',29,'employee');



delete from auth_group_permissions;
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(1,5,93);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(2,4,93);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(3,3,93);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(4,2,93);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(5,1,93);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(6,3,85);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(7,4,86);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(8,2,19);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(9,1,19);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(10,5,94);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(11,4,20);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(12,3,20);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(13,1,54);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(14,1,2);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(15,1,1);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(16,5,161);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(17,1,161);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(18,1,18);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(19,1,11);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(20,1,12);
insert  into `auth_group_permissions`(`id`,`group_id`,`permission_id`) values 
(21,1,13);




delete from sad_menu;
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(1,'DBM','Sistema','#',90,'icon-cogs',1,NULL,'2013-10-31 04:59:29','2013-10-31 05:02:12',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(2,'DBM','Recursos','sad/resource/index/',901,'icon-lock',1,NULL,'2013-10-31 05:02:06','2013-10-31 05:02:06',16,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(3,'DBM','Perfiles','sad/group/index/',902,'icon-group',1,NULL,'2013-10-31 05:03:15','2013-10-31 05:03:15',17,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(4,'DBM','Permisos','sad/group/permissions_edit/',903,'icon-magic',1,NULL,'2013-10-31 05:04:35','2013-10-31 05:04:35',17,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(5,'DBM','Modulos','sad/module/index/',904,'icon-hdd',1,NULL,'2013-10-31 05:08:29','2013-10-31 05:08:29',14,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(6,'DBM','Soluciones','space/solution/index/',905,'icon-wrench',1,NULL,'2013-10-31 05:09:23','2013-10-31 05:09:23',10,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(7,'DBM','Planes','sad/module/plans_edit/',906,'icon-magic',1,NULL,'2013-10-31 05:10:15','2013-10-31 05:10:15',14,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(8,'DBM','Menus','sad/menu/index/',907,'icon-list',1,NULL,'2013-10-31 05:10:49','2013-10-31 05:10:49',15,1);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(9,'DBM','Cuenta','#',80,'icon-wrench',1,NULL,'2013-10-31 05:12:15','2013-11-10 17:14:05',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(10,'DBM','Asociacion','space/association/edit_current/',801,'icon-briefcase',1,NULL,'2013-10-31 05:17:03','2013-10-31 05:17:03',11,9);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(11,'DBM','Empresas','space/enterprise/index/',802,'icon-sitemap',1,NULL,'2013-10-31 05:18:06','2013-10-31 05:18:06',12,9);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(12,'DBM','Empresa','space/enterprise/edit_current/',803,'icon-briefcase',1,NULL,'2013-10-31 05:18:46','2013-10-31 05:18:46',12,9);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(13,'DBM','Sedes','space/headquart/index/',804,'icon-sitemap',1,NULL,'2013-10-31 05:19:25','2013-10-31 05:19:25',13,9);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(14,'DBM','Usuarios','sad/user/index/',805,'icon-user',1,NULL,'2013-10-31 05:21:51','2013-10-31 05:21:51',18,9);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(15,'DBM','Dashboard','#',10,'icon-home',1,NULL,'2013-10-31 05:24:35','2013-11-10 17:14:01',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(16,'DBM','Dashboard','mod_backend/dashboard/',101,'icon-home',1,NULL,'2013-10-31 05:29:35','2013-10-31 05:29:35',19,15);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(17,'VENTAS','Dashboard','#',10,'icon-home',1,NULL,'2013-10-31 05:38:05','2013-10-31 05:38:05',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(18,'VENTAS','Dashboard','mod_ventas/dashboard/',101,'icon-home',1,NULL,'2013-10-31 05:38:44','2013-11-25 22:00:49',20,17);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(19,'DBM','Ciudades','params/locality/index/',806,'',1,NULL,'2013-10-31 05:49:17','2013-10-31 05:49:17',3,9);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(20,'VENTAS','Maestros','#',30,'icon-calendar',1,NULL,'2013-11-01 15:41:28','2013-11-01 15:41:28',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(21,'VENTAS','Productos','maestros/producto/index/',301,'icon-print',1,NULL,'2013-11-01 15:42:22','2013-11-19 16:43:11',85,20);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(22,'PRO','Dashboard','#',10,'icon-home',1,NULL,'2013-11-20 22:25:44','2013-11-20 22:40:39',NULL,NULL);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(23,'PRO','Dashboard','mod_pro/dashboard/',101,'icon-home',1,NULL,'2013-11-20 22:40:31','2013-11-20 22:46:35',94,22);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(24,'PRO','Datos Empleado','rrhh/employee/edit/',102,'icon-briefcase',1,NULL,'2013-11-20 22:53:25','2013-11-25 10:42:25',161,22);
insert  into `sad_menu`(`id`,`module`,`title`,`url`,`pos`,`icon`,`is_active`,`description`,`registered_at`,`modified_in`,`permission_id`,`parent_id`) values 
(25,'PRO','Listado de Empleados','rrhh/employee/index/',103,'icon-calendar',1,NULL,'2013-11-21 00:04:06','2013-11-21 00:04:06',161,22);

